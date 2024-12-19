import IconsMapType from 'lazyUtils/LazyIconImport/LazyIconImport.types';

export interface ButtonProps {
  type: 'button' | 'icon';
  icon?: keyof IconsMapType;
  className?: string;
  children?: string;
  onClick?: () => void;
}
