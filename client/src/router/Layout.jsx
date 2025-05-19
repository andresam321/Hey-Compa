import { useEffect, useState } from "react";
import { Outlet } from "react-router-dom";
import { useDispatch } from "react-redux";
import { ModalProvider, Modal } from "../context/Modal";
import { thunkAuthenticate } from "../redux/session";
import Navigation from "../components/Navigation/Navigation";
import './Layout.css'; // Import the CSS for layout

export default function Layout() {
  const dispatch = useDispatch();
  const [isLoaded, setIsLoaded] = useState(false);
console.log("Layout loaded", isLoaded);

  useEffect(() => {
    dispatch(thunkAuthenticate()).then(() => setIsLoaded(true));
  }, [dispatch]);

  return (
    <div className="layout-container">
      <ModalProvider>
        <Navigation />
        <div className="content-container">
          {isLoaded && <Outlet />}
          {/* <Outlet /> */}
          <Modal />
        </div>
      </ModalProvider>
    </div>
  );
}