import { LazyIconMapType } from "lazyUtils/LazyIcon/LazyIcon.types";

export interface ButtonProps {
  type: 'button' | 'icon';
  iconName?: keyof LazyIconMapType;
  className?: string;
  children?: string;
  onClick?: () => void;
}
