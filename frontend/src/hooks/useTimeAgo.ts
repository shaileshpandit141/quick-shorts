import { useState, useEffect } from "react";

function getTimeAgo(dateStr: string): string {
  const now = new Date();
  const date = new Date(dateStr);
  const diffMs = now.getTime() - date.getTime();

  const seconds = Math.floor(diffMs / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);

  if (seconds < 60) return `${seconds} Seconds ago`;
  if (minutes < 60) return `${minutes} Minutes ago`;
  if (hours < 24) return `${hours} Hours ago`;
  return `${days} Days ago`;
}

export function useTimeAgo(dateStr: string): string {
  const [timeAgo, setTimeAgo] = useState<string>(() => getTimeAgo(dateStr));

  useEffect(() => {
    const interval = setInterval(() => {
      setTimeAgo(getTimeAgo(dateStr));
    }, 60000); // Update every 60 seconds

    return () => clearInterval(interval);
  }, [dateStr]);

  return timeAgo;
}
