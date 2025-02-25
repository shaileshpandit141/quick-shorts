/**
 * Custom hook to select toast notifications from the Redux store
 * @returns An array of toast notifications from the Redux state
 */
import { RootState } from "store/rootReducer";
import { useSelector } from "react-redux";

export const useToastSelector = () => {
  return useSelector((state: RootState) => state.toast.toasts);
};
