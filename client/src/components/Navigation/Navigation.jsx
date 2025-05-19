import { NavLink } from "react-router-dom";
import { useModal } from "../../context/Modal";
import { useSelector } from 'react-redux';
// import { useDispatch } from "react-redux";
import LoginFormModal from "../LoginFormModal/LoginFormModal";
import "../Styles/Navigation.css";

function Navigation() {
// const dispatch = useDispatch();
const { setModalContent } = useModal();
const user = useSelector((state) => state.session.user); 


// navigate to different chats ??
  const openLoginModal = () => {
    setModalContent(<LoginFormModal />);
  };

  return (
    <nav className="navbar">

      <ul className="nav-menu">
        <li className="nav-item">
          <NavLink to="/" className="nav-link">Home</NavLink>
        </li>
         {!user && (
          <li className="nav-item">
            <button className="nav-link" onClick={openLoginModal}>
              Login
            </button>
          </li>
        )}
            
      </ul>

    </nav>
  );
}


export default Navigation;
