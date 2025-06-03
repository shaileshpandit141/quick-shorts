import React, { FC, JSX } from "react";
import "./VideoOwnerCard.css";
import { Button } from "components/Common";

interface VideoOwnerCardProps {}

const VideoOwnerCard: FC<VideoOwnerCardProps> = (props): JSX.Element => {
  return (
    <div className="video-owner-card">
      <section className="video-owner-card-header">
        <div className="user-profile-container">
          <figure className="figure"></figure>
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
          <Button type="button" className="follow-button">
            Follow
          </Button>
        </div>
      </section>
      <section className="video-owner-card-body">
        <div className="scroll-body">
          <p className="caption">
            Lorem ipsum, dolor sit amet consectetur adipisicing elit. Explicabo
            dicta distinctio id quas fuga assumenda?
          </p>
          <section className="tag-container">
            <span>#dev</span>
            <span>#python</span>
            <span>#learning</span>
          </section>
        </div>
      </section>
      <section className="video-action-btns-container">
        <div className="btn-container">
          <Button type="icon" icon="thumbUp" />
          <label htmlFor="">23K</label>
        </div>
        <div className="btn-container">
          <Button type="icon" icon="thumbDown" />
          <label htmlFor="">5K</label>
        </div>
        <div className="btn-container">
          <Button type="icon" icon="comment" />
          <label htmlFor="">1M</label>
        </div>
      </section>
    </div>
  );
};

export default VideoOwnerCard;
