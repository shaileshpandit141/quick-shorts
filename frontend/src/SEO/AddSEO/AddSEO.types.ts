export interface AddSEOProps {
  title: string;
  description: string;
  keywords?: string;
  canonical?: string;
  robots?: string;
  metaTags?: { [key: string]: string };
}
