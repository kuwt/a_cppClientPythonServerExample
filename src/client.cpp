/* 
* Written by kuwingto, 10 March 2019
*/

#include <string.h>
#include <stdio.h>
#include <chrono>  // for high_resolution_clock
#include <math.h>
#include <opencv2/opencv.hpp>
#include <zmq.hpp>
#include "my_message.pb.h"

int main()
{
	GOOGLE_PROTOBUF_VERIFY_VERSION;
	zmq::context_t m_context = zmq::context_t(1);
	zmq::socket_t *m_pSock;

	/****** start service **********/
	m_pSock = new zmq::socket_t(m_context, ZMQ_REQ);
	m_pSock->connect("tcp://localhost:5555");
	int linger = 0;
	m_pSock->setsockopt(ZMQ_LINGER, &linger, sizeof(linger));

	cv::Mat img;
	img = cv::imread("../data/test.bmp", CV_LOAD_IMAGE_GRAYSCALE);
	
	my_message sendPack;
	sendPack.set_class_id(0);
	my_message_Mat sendMat;
	sendMat.set_width(img.size().width);
	sendMat.set_height(img.size().height);
	sendMat.set_image_data((char *)img.data, sizeof(uchar) * img.size().width * img.size().height);
	std::string s1 = sendMat.SerializeAsString();
	std::cout << "s1.size() = " << s1.size() << "\n";
	sendPack.set_allocated_img(&sendMat);
	std::string s = sendPack.SerializeAsString();
	std::cout << "s.size() = " << s.size() << "\n";
	/***********************
	//  Send
	**********************/
	{
		zmq::message_t message(s.size());
		memcpy(message.data(), s.data(), s.size());
		m_pSock->send(message);
	}
	sendPack.release_img();
	/***********************
	// get reply
	**********************/
	zmq::pollitem_t items[] = { { *m_pSock, 0, ZMQ_POLLIN, 0 } };
	zmq::poll(&items[0], 1, 5 * 1000);

	if (items[0].revents & ZMQ_POLLIN)
	{
		zmq::message_t reply;
		if (m_pSock->recv(&reply, 0))
		{
			
			std::string  msgStr = std::string((char*)reply.data(), reply.size());
			//std::cout << msgStr << "\n";
			
			//unserialize
			my_message out;
			out.ParseFromString(msgStr);

			int class_id = out.class_id();
			std::cout << "class_id = " << class_id << "\n";
			int width = out.img().width();
			int height = out.img().height();
			std::cout << "width = " << width << " height = " << height << "\n";
			cv::Mat img = cv::Mat(height,width, CV_8UC1);
			memcpy(img.data, &out.img().image_data()[0], sizeof(uchar) * width * height);

			cv::imshow("img",img);
			cv::waitKey(1);
		}
		else
		{
			std::cout << "reply from server malformed! \n";
			return -1;
		}
	}
	else
	{
		std::cout << "No response from server \n";
		m_pSock->close();
		m_pSock = new zmq::socket_t(m_context, ZMQ_REQ);
		m_pSock->connect("tcp://localhost:5555");
		int linger = 0;
		m_pSock->setsockopt(ZMQ_LINGER, &linger, sizeof(linger));

	}


	std::cout << "press to continue \n";
	getchar();

	m_pSock->close();
	delete m_pSock;
    return 0;
}

