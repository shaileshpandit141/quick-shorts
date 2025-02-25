import { useEffect, useMemo } from "react";
import { AddSEOProps } from "./AddSEO.types";
import { metaConfig } from "SEO/metaConfig/metaConfig";

export const AddSEO: React.FC<AddSEOProps> = ({
  title,
  description,
  keywords,
  canonical,
  robots = "index, follow",
  metaTags = {},
}) => {
  const appName = metaConfig.appName;

  // Function to update or create meta tags
  const updateMetaTag = (name: string, content: string, isProperty = false) => {
    if (!content) return; // Avoid setting empty values

    let metaTag = document.querySelector(
      isProperty ? `meta[property="${name}"]` : `meta[name="${name}"]`,
    );

    if (!metaTag) {
      metaTag = document.createElement("meta");
      isProperty
        ? metaTag.setAttribute("property", name)
        : metaTag.setAttribute("name", name);
      document.head.appendChild(metaTag);
    }
    metaTag.setAttribute("content", content);
  };

  // Memoize meta tag data to prevent unnecessary updates
  const metaData = useMemo(
    () => ({
      title: title ? `${appName} │ ${title}` : appName,
      description,
      keywords,
      robots,
      canonical: canonical || metaConfig.canonical,
      "og:title": title ? `${appName} • ${title}` : appName,
      "og:description": description,
      "og:type": "website",
      "og:url": window.location.href,
      "og:site_name": appName,
      "twitter:title": title ? `${appName} • ${title}` : appName,
      "twitter:description": description,
      "twitter:card": "summary_large_image",
      "twitter:site": "@mywebsite",
      ...metaConfig.metaTags,
      ...metaTags,
    }),
    [title, description, keywords, canonical, robots, metaTags, appName],
  );

  useEffect(() => {
    if (metaData.title) document.title = metaData.title;

    // Update meta tags
    Object.entries(metaData).forEach(([key, value]) => {
      if (key === "canonical") {
        let linkTag = document.querySelector(
          "link[rel='canonical']",
        ) as HTMLLinkElement;
        if (!linkTag) {
          linkTag = document.createElement("link");
          linkTag.rel = "canonical";
          document.head.appendChild(linkTag);
        }
        linkTag.href = value || "";
      } else {
        updateMetaTag(
          key,
          value || "",
          key.startsWith("og:") || key.startsWith("twitter:"),
        );
      }
    });
  }, [metaData]);

  // No UI, just updates the <head> section
  return null;
};
