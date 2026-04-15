import { useEffect, useRef } from 'react';
import axios from 'axios';
import { io } from 'socket.io-client';
import { Button, Form, FormProps, Input, notification } from 'antd';
import { MailModel } from '../../models/mail-model';
import './send-mail-page-style.css';
import { TextAreaRef } from 'antd/es/input/TextArea';
import { AuthUserModel } from '../../models/auth-user';



export const SendMailPage = () => {

    const [notificationInstance] = notification.useNotification();

    const [formInstance] = Form.useForm();

    const textAreaRef = useRef<TextAreaRef>(null);

    useEffect(() => {
        const socket = io("http://localhost:8000", {
            transports: ['websocket']
        });
        socket.on("get_acknowledgement", (message: any) => {
            if (textAreaRef.current && textAreaRef.current.resizableTextArea) {
                textAreaRef.current.resizableTextArea.textArea.value += `mail ${message.mail_uid} was send by service ${message.service_uid}\n\r`;
            }
        });

        return () => {
            socket.disconnect();
        }
    }, []);

    const onFinish: FormProps<MailModel>['onFinish'] = async (mail) => {
        const authUserJson = localStorage.getItem('authUser');
        let authUser: AuthUserModel | null = null;

        if (authUserJson) {
            authUser = JSON.parse(authUserJson);
        }

        if (authUser) {
            try {
                await axios.request({
                    method: 'POST',
                    data: mail,
                    url: 'http://127.0.0.1:8000/mail-services',
                    headers: { 'Authorization': `Bearer ${authUser.token}` }
                });
                notificationInstance.success({
                    message: `Notification`,
                    description: 'Message was sent succesfully!',
                });
            } catch {
                notificationInstance.error({
                    message: `Notification`,
                    description: 'Message was sent with a critical error.',
                });
            }
        }
    };

    return (
        <div className='mail-page-main-container'>
            <h2>Send mail page</h2>
            <Form className='mail-form' form={formInstance} layout={'vertical'} onFinish={onFinish}>
                <Form.Item<MailModel>
                    name="uid"
                    initialValue={''}
                    hidden
                >
                    <Input type='hidden' />
                </Form.Item>

                <Form.Item<MailModel>
                    label="Sender"
                    name="sender"
                    rules={[{ required: true, message: 'Please input your sender!' }]}
                    initialValue={'me'}
                >
                    <Input />
                </Form.Item>

                <Form.Item<MailModel>
                    label="Reciever"
                    name="reciever"
                    rules={[{ required: true, message: 'Please input your reciever!' }]}
                    initialValue={'you'}
                >
                    <Input />
                </Form.Item>

                <Form.Item<MailModel>
                    label='Message'
                    name="message"
                    initialValue={'Hello world!'}
                >
                    <Input />
                </Form.Item>

                <Form.Item>
                    <Button type="primary" htmlType="submit">
                        Submit
                    </Button>
                </Form.Item>
                <div>
                    <Input.TextArea rows={4} ref={textAreaRef}></Input.TextArea>
                </div>
            </Form>
        </div>

    );
}