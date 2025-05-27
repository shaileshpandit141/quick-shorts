import React, { FC, JSX } from "react";
import "./ShortVideoPlayer.css";
import Video from "../Video/Video"

interface ShortVideoPlayerProps { }

const ShortVideoPlayer: FC<ShortVideoPlayerProps> = (props): JSX.Element => {
  return (
    <div className="short-video-player">
      <Video />
      <Video />
      <Video />
    </div>
  )
}

export default ShortVideoPlayer;
