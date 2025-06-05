import React, { FC, JSX } from "react";
import "./ShortsPage.css";
import { AddSEO } from "SEO";
import Video from "components/Pages/Shorts/Video";
import data from "data.json";

const ShortsPage: FC<{}> = (): JSX.Element => {
  return (
    <div className="shorts-page">
      <AddSEO title="Shorts" description="This page containe short videos." />
      <div className="shorts-video-player">
        {data.results.map((shorts, index) => (
          <Video
            key={index}
            shorts_id={index}
          />
        ))}
      </div>
    </div>
  );
};

export default ShortsPage;
