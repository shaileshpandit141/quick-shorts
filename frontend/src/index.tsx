import React from "react";
import ReactDOM from "react-dom/client";
import { Provider } from "react-redux";
import { store } from "store";
import { RootProvider } from "contexts/Providers";
import App from "./App";
import "./styles/index.css";
import * as serviceWorkerRegistration from "./serviceWorkerRegistration";

const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement,
);
root.render(
  <Provider store={store}>
    <RootProvider>
      <React.StrictMode>
        <App />
      </React.StrictMode>
    </RootProvider>
  </Provider>,
);

// Register the pwa service worker
serviceWorkerRegistration.register();
