import React, { FC, JSX } from "react";
import "./Shorts.css";
import { AddSEO } from "SEO";
import { VideoPlayer } from "components";

interface ShortsProps {}

const Shorts: FC<ShortsProps> = (props): JSX.Element => {
  return (
    <div className="shorts">
      <AddSEO title="Shorts" description="This page containe short videos." />
      <VideoPlayer />
      {/* <h1>Shorts</h1> */}
    </div>
  );
};

export default Shorts;
