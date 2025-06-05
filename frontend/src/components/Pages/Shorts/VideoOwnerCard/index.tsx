import React, { FC, JSX, useState } from "react";
import "./VideoOwnerCard.css";
import { Button } from "components/Common";
import { useIsCommentsOpen } from "contexts/features/IsCommentsOpen";
import data from "data.json";
import { useTimeAgo } from "hooks/useTimeAgo";
import { useNumberFormatter } from "hooks/useNumberFormatter";

interface VideoOwnerCardProps {
  shorts_id: number;
}

const VideoOwnerCard: FC<VideoOwnerCardProps> = (props): JSX.Element => {
  const [isCaptionOpen, setIsCaptionOpen] = useState(false);
  const { toggleIsCommentsOpen } = useIsCommentsOpen();
  const shorts = data.results[props.shorts_id];
  const timeAgo = useTimeAgo(shorts.updated_at);
  const numberFormatter = useNumberFormatter();

  const toggleIsCaptionOpen = (event: React.MouseEvent<HTMLElement>) => {
    setIsCaptionOpen((prevState) => !prevState);
  };

  return (
    <div className="video-owner-card">
      <section className="video-owner-card-header">
        <div className="user-profile-container">
          <figure className="figure"></figure>
        </div>
        <div className="user-info">
          <label className="username">{shorts.owner.username}</label>
          <div className="shorts-info">
            <span className="views">
              {numberFormatter(shorts.total_views)} Views
            </span>
            <span className="dot"></span>
            <span className="date">{timeAgo}</span>
          </div>
        </div>
        <div className="action-buttons">
          <Button type="button" className="follow-button">
            Follow
          </Button>
        </div>
      </section>
      <section className="video-owner-card-body">
        <div
          className={`scroll-body ${isCaptionOpen && "active"}`}
          onClick={toggleIsCaptionOpen}
        >
          <p className="caption">{shorts.caption}</p>
          <section className="tag-container">
            {shorts.tags.map((tag) => (
              <span key={tag.id}>#{tag.name}</span>
            ))}
          </section>
        </div>
      </section>
      <section className="video-action-btns-container">
        <div className="btn-container">
          <Button type="icon" icon="thumbUp" />
          <label htmlFor="">{numberFormatter(shorts.total_likes)}</label>
        </div>
        {/* <div className="btn-container">
          <Button type="icon" icon="thumbDown" />
          <label htmlFor="">5K</label>
        </div> */}
        <div className="btn-container" onClick={toggleIsCommentsOpen}>
          <Button type="icon" icon="comment" />
          <label htmlFor="">{numberFormatter(shorts.total_comments)}</label>
        </div>
      </section>
    </div>
  );
};

export default VideoOwnerCard;
