import React from "react";
import ReactDOM from "react-dom/client";
import { Provider } from "react-redux";   
import { RouterProvider } from "react-router-dom";
import configureStore from "./redux/store";
import { router } from "./router/Index";
import * as sessionActions from "./redux/session";
import "./index.css";

const store = configureStore();

if (import.meta.env.MODE !== "production") {
  window.store = store;
  window.sessionActions = sessionActions;
}

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <Provider store={store}>
      <RouterProvider router={router} />
    </Provider>
  </React.StrictMode>
);

