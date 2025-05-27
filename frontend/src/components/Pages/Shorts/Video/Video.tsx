import React, { FC, JSX, useEffect, useRef } from "react";
import "./Video.css";
import { Button } from "components";
import { useVideo } from "contexts/features/VideoContext";

interface VideoProps { }

const Video: FC<VideoProps> = (props): JSX.Element => {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const { isMuted, toggleMute } = useVideo();

  useEffect(() => {
    const currentVideoRef = videoRef.current;

    if (currentVideoRef) {
      currentVideoRef.muted = isMuted;
    }

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          currentVideoRef?.play().catch(error => {
            console.error('Error playing video:', error);
          });
        } else {
          currentVideoRef?.pause();
        }
      });
    }, {
      threshold: 0.5
    });

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
            icon={
              isMuted ? "volumeOff" : "volumeOn"
            }
            onClick={toggleMute}
          />
        </div>
        <div className="video-owner-info">
          <section className="video-owner-info-header">
            <div className="user-profile-container">
              <figure className="figure">

              </figure>
            </div>
            <div className="user-info">
              <label className="username">Username</label>
              <div className="shorts-info">
                <span className="views">50K Views</span>
                <span className="dot"></span>
                <span className="date">8 Days ago</span>
              </div>
            </div>
            <div className="action-buttons">
              <Button type="button" className="follow-button">Follow</Button>
            </div>
          </section>
          <section className="video-owner-info-body">
            <p>
              Lorem ipsum, dolor sit amet consectetur adipisicing elit.
              Explicabo dicta distinctio id quas fuga assumenda?
            </p>
          </section>
        </div>
        <video
          src="http://localhost:8000/api/v1/shorts/videos/streams/3/"
          ref={videoRef}
          muted
          playsInline
          loop
          onClick={handleMute}
        >
          Your Browser is not supported the video tag
        </video>
      </div>
    </div>
  )
}

export default Video;
