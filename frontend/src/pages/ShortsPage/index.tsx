import React, { FC, JSX } from "react";
import "./ShortsPage.css";
import { AddSEO } from "SEO";
import { VideoPlayer } from "components";

interface ShortsPageProps {}

const ShortsPage: FC<ShortsPageProps> = (props): JSX.Element => {
  return (
    <div className="shorts">
      <AddSEO title="Shorts" description="This page containe short videos." />
      <VideoPlayer />
    </div>
  );
};

export default ShortsPage;
