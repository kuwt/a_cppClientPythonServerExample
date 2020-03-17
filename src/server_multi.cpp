/* 
* Written by kuwingto, 10 March 2019
*/

#include <string.h>
#include <stdio.h>
#include <chrono>  // for high_resolution_clock
#include <math.h>
#include <opencv2/opencv.hpp>
#include <zmq.hpp>
#include "my_message_multi.pb.h"

int main()
{
	GOOGLE_PROTOBUF_VERIFY_VERSION;
	zmq::context_t m_context = zmq::context_t(1);
	zmq::socket_t *m_pSock;

	/****** start service **********/
	m_pSock = new zmq::socket_t(m_context, ZMQ_REP); // rep for server
	m_pSock->bind("tcp://*:5555");

	/************ service loop ***************/
	while (true)
	{
		std::cout << "waiting connection...\n";
		zmq::message_t request;
		if (m_pSock->recv(&request, 0))
		{
			std::cout << "receive message...\n";
			/************ receive message ***************/
			std::string  msgStr = std::string((char*)request.data(), request.size());
			//unserialize
			my_message_multi out;
			out.ParseFromString(msgStr);

			int class_id = out.class_id();
			std::cout << "class_id = " << class_id << "\n";
			for (int i = 0; i < out.imgs_size(); ++i)
			{
				int width = out.imgs(i).width();
				int height = out.imgs(i).height();
				std::cout << "width = " << width << " height = " << height << "\n";
				cv::Mat img = cv::Mat(height, width, CV_8UC1);
				memcpy(img.data, &out.imgs(i).image_data()[0], sizeof(uchar) * width * height);

				cv::imshow("img" + std::to_string(i), img);
				cv::waitKey(1);
			}

			/************ prepare reply ***************/
			cv::Mat img;
			img = cv::imread("../data/test.bmp", CV_LOAD_IMAGE_GRAYSCALE);

			my_message_multi sendPack;
			sendPack.set_class_id(1);

			my_message_multi_Mat* sendMat = sendPack.add_imgs();
			(*sendMat).set_width(img.size().width);
			(*sendMat).set_height(img.size().height);
			(*sendMat).set_image_data((char *)img.data, sizeof(uchar) * img.size().width * img.size().height);
			std::string s1 = (*sendMat).SerializeAsString();
			std::cout << "s1.size() = " << s1.size() << "\n";

			std::string s = sendPack.SerializeAsString();
			std::cout << "s.size() = " << s.size() << "\n";
			/************ send reply  ***************/
			{
				zmq::message_t message(s.size());
				memcpy(message.data(), s.data(), s.size());
				m_pSock->send(message);
			}
		}
	}

	std::cout << "press to continue \n";
	getchar();

	m_pSock->close();
	delete m_pSock;
    return 0;
}

