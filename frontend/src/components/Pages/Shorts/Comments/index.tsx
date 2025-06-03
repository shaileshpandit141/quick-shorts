import React, { FC, JSX } from "react";
import "./Comments.css";
import { Drawer, Button, Input } from "components";
import { useIsCommentsOpen } from "contexts/features/IsCommentsOpen";

interface CommentsProps {}

const Comments: FC<CommentsProps> = (props): JSX.Element => {
  const { isCommentsOpen, toggleIsCommentsOpen } = useIsCommentsOpen();

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
            Comments <span>1M</span>
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
            <p>Lorem ipsum dolor sit amet.</p>
            <p>Lorem ipsum dolor sit amet.</p>
            <p>Lorem ipsum dolor sit amet.</p>
          </div>
        </section>
        <form className="comment-form">
          <Input type="text" name="comment" value={""} onChange={() => {}} />
          <Button type="icon" icon="send" className="submit-btn">
            Submit
          </Button>
        </form>
      </div>
    </Drawer>
  );
};

export default Comments;
