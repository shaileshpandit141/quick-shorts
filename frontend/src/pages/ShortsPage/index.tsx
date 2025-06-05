import React, { FC, JSX } from "react";
import "./ShortsPage.css";
import { AddSEO } from "SEO";
import Video from "components/Pages/Shorts/Video";

interface ShortsPageProps { }

const ShortsPage: FC<ShortsPageProps> = (props): JSX.Element => {
  return (
    <div className="shorts-page">
      <AddSEO title="Shorts" description="This page containe short videos." />
      <div className="shorts-video-player">
        {Array(5).fill(0).map((_, index) => (
          <Video key={index} />
        ))}
      </div>
    </div>
  );
};

export default ShortsPage;
