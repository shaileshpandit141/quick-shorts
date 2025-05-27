import React, { FC, JSX } from "react";
import "./Shorts.css";
import { AddSEO } from "SEO";
import { ShortVideoPlayer } from "components";

interface ShortsProps { }

const Shorts: FC<ShortsProps> = (props): JSX.Element => {
  return (
    <div className="shorts">
      <AddSEO title="Shorts" description="This page containe short videos." />
      <ShortVideoPlayer />
    </div>
  )
}

export default Shorts;
