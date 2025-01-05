import React, { useEffect } from "react";
import "./Toast.css"
import { useDispatch } from "react-redux";
import { removeToast } from "features/toast";
import { LazyIcon } from "lazyUtils/LazyIcon/LazyIcon";

interface ToastProps {
  id: string;
  type: "success" | "error" | "info" | "warning";
  message: string;
  duration?: number;
}

const Toast: React.FC<ToastProps> = ({ id, type, message, duration = 5000 }) => {
  const dispatch = useDispatch();

  useEffect(() => {
    const timer = setTimeout(() => {
      dispatch(removeToast(id));
    }, duration);

    return () => clearTimeout(timer);
  }, [dispatch, id, duration]);

  return (
    <div className={`toast toast-${type}`}>
      <section className="toast-icon-container">
        <div className="icon-container">
          <LazyIcon iconName={type} />
        </div>
      </section>
      <section className="message-container">
        <p className="error-message">{message}</p>
      </section>
      <section className="button-container">
        <button
          className="toast-close-button"
          onClick={() => dispatch(removeToast(id))}
        >
          <div className="icon-container">
            <LazyIcon iconName="close" />
          </div>
        </button>
      </section>
    </div>
  );
};

export default Toast;
