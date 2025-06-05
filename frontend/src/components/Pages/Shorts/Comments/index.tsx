import React, { FC, JSX } from "react";
import "./Comments.css";
import { Drawer, Button, Input } from "components";
import { useIsCommentsOpen } from "contexts/features/IsCommentsOpen";
import data from "data.json";
import { useNumberFormatter } from "hooks/useNumberFormatter";

interface CommentsProps {
  shorts_id: number;
}

const Comments: FC<CommentsProps> = (props): JSX.Element => {
  const { isCommentsOpen, toggleIsCommentsOpen } = useIsCommentsOpen();
  const shorts = data.results[props.shorts_id]
  const numberFormatter = useNumberFormatter()

  return (
    <Drawer
      isOpen={isCommentsOpen}
      className="comments-page"
      position="absolute"
      onClick={toggleIsCommentsOpen}
    >
      <div className={`comments-wrapper ${isCommentsOpen && "active"}`}>
        <section className="comments-header">
          <h4 className="comment-title">
            Comments <span>{numberFormatter(shorts.total_comments)}</span>
          </h4>
          <Button
            type="button"
            className="close-btn"
            onClick={toggleIsCommentsOpen}
          >
            Close
          </Button>
        </section>
        <section className="comments-container">
          <div className="comments-scroll-wrapper">
            {/* This is a actual comment card TSX */}
            <div className="comment-container">
              <section className="comment-header">
                <figure className="figure">f</figure>
                <div className="comment-info">
                  <span className="username">Username</span>
                  <span className="time">8 Days ago</span>
                </div>
              </section>
              <section className="comment-contnet">
                <div className="curve-line">
                  <span className="span-1"></span>
                  <span className="span-2"></span>
                </div>
                <div className="content-box">
                  <p className="content">
                    Lorem ipsum dolor sit amet consectetur adipisicing elit.
                    Doloremque vel error, consequuntur sed consectetur rem.
                    Lorem ipsum dolor sit amet, consectetur adipisicing elit.
                    Provident odit voluptate beatae perferendis culpa,
                    architecto dicta quis illum possimus sit!
                  </p>
                </div>
              </section>
            </div>
          </div>
        </section>
        <form className="comment-form">
          <Input type="text" name="comment" value={""} onChange={() => { }} />
          <Button type="icon" icon="send" className="submit-btn">
            Submit
          </Button>
        </form>
      </div>
    </Drawer>
  );
};

export default Comments;
