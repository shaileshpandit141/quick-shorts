import React, { FC, JSX, useEffect, useRef } from "react";
import "./Video.css";
import { Button } from "components";
import { useVideo } from "contexts/features/VideoContext";
import VideoOwnerCard from "../VideoOwnerCard";
import Comments from "../Comments";
import data from "data.json";

interface VideoProps {
  shorts_id: number;
}

const Video: FC<VideoProps> = (props): JSX.Element => {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const { isMuted, toggleMute } = useVideo();
  const shorts = data.results[props.shorts_id]

  useEffect(() => {
    const currentVideoRef = videoRef.current;

    if (currentVideoRef) {
      currentVideoRef.muted = isMuted;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            currentVideoRef?.play().catch((error) => {
              console.error("Error playing video:", error);
            });
          } else {
            currentVideoRef?.pause();
          }
        });
      },
      {
        threshold: 0.5,
      },
    );

    if (currentVideoRef) {
      observer.observe(currentVideoRef);
    }

    // Cleanup observer on component unmount
    return () => {
      if (currentVideoRef) {
        observer.unobserve(currentVideoRef);
      }
    };
  }, [isMuted]);

  const handleMute = (event: React.MouseEvent<HTMLElement>) => {
    event.preventDefault();
    toggleMute();
  };

  return (
    <div className="video-container">
      <div className="video-player-container">
        <div className="video-header-container">
          <Button
            type="icon"
            icon={isMuted ? "volumeOff" : "volumeOn"}
            onClick={toggleMute}
          />
        </div>
        <video
          src={`http://localhost:8000/api/v1/shorts/videos/streams/${shorts.id}/`}
          ref={videoRef}
          muted
          playsInline
          loop
          onClick={handleMute}
        >
          Your Browser is not supported the video tag
        </video>
        <VideoOwnerCard
          shorts_id={props.shorts_id}
        />
        <Comments
          shorts_id={props.shorts_id}
        />
      </div>
    </div>
  );
};

export default Video;
