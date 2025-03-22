import React, { useEffect, useState } from "react";
import "./Toast.css";
import { useDispatch } from "react-redux";
import { removeToast } from "features/toast";
import { RenderLazyIcon } from "lazyUtils";

interface ToastProps {
  id: string;
  type: "success" | "error" | "info" | "warning";
  message: string;
  duration?: number;
}

const Toast: React.FC<ToastProps> = ({
  id,
  type,
  message,
  duration = 5000,
}) => {
  const dispatch = useDispatch();
  const [isRemoving, setIsRemoving] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsRemoving(true);
      setTimeout(() => {
        dispatch(removeToast(id));
      }, 300);
    }, duration);

    return () => clearTimeout(timer);
  }, [dispatch, id, duration]);

  const handleClose = () => {
    setIsRemoving(true);
    setTimeout(() => {
      dispatch(removeToast(id));
    }, 300);
  };

  return (
    <div className={`toast toast-${type} ${isRemoving ? "toast-removed" : ""}`}>
      <section className="toast-icon-container">
        <div className="icon-container">
          <RenderLazyIcon icon={type} />
        </div>
      </section>
      <section className="message-container">
        <p className="error-message">{message}</p>
      </section>
      <section className="button-container">
        <button className="toast-close-button" onClick={handleClose}>
          <div className="icon-container">
            <RenderLazyIcon icon="close" />
          </div>
        </button>
      </section>
    </div>
  );
};

export default Toast;
