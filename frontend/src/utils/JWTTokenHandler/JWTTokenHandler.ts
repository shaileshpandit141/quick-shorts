import { JWTHeader, JWTPayload, DecodedJWT } from "./JWTTokenHandler.types";

export class JWTTokenHandler {
  token: string;

  constructor(token: string) {
    this.token = token;
  }

  decode(): DecodedJWT | null {
    try {
      const [header, payload, signature] = this.token.split(".");

      const decodeBase64Url = (str: string): any => {
        str = str.replace(/-/g, "+").replace(/_/g, "/");
        const pad = str.length % 4;
        if (pad) {
          str += "=".repeat(4 - pad);
        }
        return JSON.parse(atob(str));
      };

      const decodedHeader: JWTHeader = decodeBase64Url(header);
      const decodedPayload: JWTPayload = decodeBase64Url(payload);

      return {
        header: decodedHeader,
        payload: decodedPayload,
        signature: signature,
      };
    } catch (error) {
      console.error("Invalid JWT token:", error);
      return null;
    }
  }

  isTokenExpired(): boolean {
    try {
      const decoded = this.decode();
      if (!decoded || !decoded.payload || !decoded.payload.exp) {
        return true; // Consider it expired/invalid if no expiration info
      }

      // exp is in seconds, Date.now() is in milliseconds, so convert
      const expirationDate = decoded.payload.exp * 1000;
      const currentDate = Date.now();

      return currentDate > expirationDate;
    } catch (error) {
      console.error("Error checking token expiration:", error);
      return true; // Consider it expired if there's an error
    }
  }
}
