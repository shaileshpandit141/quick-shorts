import { useCallback } from "react";

type FormatOptions = {
  decimals?: number;
};

export const useNumberFormatter = () => {
  const formatNumber = useCallback(
    (num: number, options: FormatOptions = {}) => {
      const { decimals = 1 } = options;

      if (num < 1000) return num.toString();

      const units = ["K", "M", "B", "T"];
      let unitIndex = -1;
      let reducedNum = num;

      while (reducedNum >= 1000 && unitIndex < units.length - 1) {
        reducedNum /= 1000;
        unitIndex++;
      }

      return `${parseFloat(reducedNum.toFixed(decimals))}${units[unitIndex]}`;
    },
    []
  );

  return formatNumber;
};
