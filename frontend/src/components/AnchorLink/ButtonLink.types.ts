import { LazyIconMapType } from "lazyUtils/LazyIcon/LazyIcon.types";

export interface ButtonLinkProps {
  to: string;
  type: 'link' | 'icon';
  iconName?: keyof LazyIconMapType;
  className?: string;
  children?: string;
}
