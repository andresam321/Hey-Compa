import { createBrowserRouter } from 'react-router-dom';
import Layout from './Layout';
import ChatWindow from '../components/Chat/ChatWindow';

export const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      {
        path: "/",
        element: <ChatWindow />,
      },

    ],
  },
]);