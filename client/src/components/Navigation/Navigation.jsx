import { NavLink } from "react-router-dom";
import { useEffect } from 'react'
import { useSelector } from 'react-redux';
import { useDispatch } from "react-redux";
// import LoginFormModal from "../LoginFormModal/LoginFormModal";
import "./Navigation.css";

function Navigation() {
const dispatch = useDispatch();
const user = useSelector((state) => state.session.user); 

// navigate to different chats ??

  return (
    <nav className="navbar">
        {user && (
      <ul className="nav-menu">
        <li className="nav-item">
          <NavLink to="/" className="nav-link">Home</NavLink>
        </li>

            
   
      </ul>
        )}
    </nav>
  );
}


export default Navigation;
