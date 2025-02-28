export interface JWTHeader {
  alg: string;
  typ: string;
  [key: string]: any;
}

export interface JWTPayload {
  exp?: number;
  iat?: number;
  [key: string]: any;
}

export interface DecodedJWT {
  header: JWTHeader;
  payload: JWTPayload;
  signature: string;
}
