import './login-page-style.css';
import axios from 'axios';
import { Button, Form, FormProps, Input } from 'antd';
import { LoginModel } from '../../models/login-model';
import { AuthUserModel } from '../../models/auth-user';
import { AppConsts } from '../../app-consts';
import { useCallback } from 'react';


export const LoginPage = () => {

    const getAuthUserAsync = useCallback(async (login: LoginModel) => {
        let authUser: AuthUserModel | null = null;
        try {
            const response = await axios.request<AuthUserModel>({
                method: 'POST',
                data: login,
                url: `${AppConsts.webAPIRoot}/auth`
            });

            authUser = response.data;
        } catch {
            authUser = null;
        }

        if (authUser) {
            window.localStorage.setItem('authUser', JSON.stringify(authUser));
        }
    }, []);

    const onFinish: FormProps<LoginModel>['onFinish'] = async (login) => {
        await getAuthUserAsync(login);
    };

    return (
        <div className='login-page-main-container'>
            <h2>LOGIN</h2>
            <Form className='login-form' layout={'vertical'} onFinish={onFinish}>
                <Form.Item<LoginModel>
                    label="Email"
                    name="email"
                    rules={[{ required: true, message: 'Please input your email!' }]}
                    initialValue={'egorleontev54@gmail.com'}
                >
                    <Input />
                </Form.Item>

                <Form.Item<LoginModel>
                    label="Password"
                    name="password"
                    rules={[{ required: true, message: 'Please input your reciever!' }]}
                    initialValue={'abcdef'}
                >
                    <Input />
                </Form.Item>

                <Form.Item>
                    <Button type="primary" htmlType="submit">
                        Submit
                    </Button>
                </Form.Item>
            </Form>
        </div>
    );
}