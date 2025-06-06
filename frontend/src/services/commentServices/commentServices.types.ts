export interface CommentParams {
  video: number;
  page?: number;
  "page-size"?: number;
}

export interface CommentCredentials {
  video: number;
  content: string;
}
