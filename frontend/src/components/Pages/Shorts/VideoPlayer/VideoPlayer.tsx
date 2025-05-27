import React, { FC, JSX } from "react";
import "./VideoPlayer.css";
import Video from "../Video/Video";

interface VideoPlayerProps {}

const VideoPlayer: FC<VideoPlayerProps> = (props): JSX.Element => {
  return (
    <div className="short-video-player">
      <Video />
      <Video />
      <Video />
    </div>
  );
};

export default VideoPlayer;
