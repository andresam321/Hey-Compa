import { createBrowserRouter } from 'react-router-dom';
import Layout from './Layout';
import LoginFormModal from '../components/LoginFormModal/LoginFormModal';

export const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      {
        path: "/",
        element: <div>Home</div>,
      },

    ],
  },
]);