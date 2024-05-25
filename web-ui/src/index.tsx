import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import { HomePage } from './pages/home-page/home-page';
import { LoginPage } from './pages/login-page/login-page';
import { SendMailPage } from './pages/send-mail-page/send-mail-page';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";


const router = createBrowserRouter([
  {
    path: "/",
    element: <HomePage />,
  },
  {
    path: '/login',
    element: <LoginPage />
  },
  {
    path: '/send-mail',
    element: <SendMailPage />
  },
]);

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);