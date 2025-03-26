import React, { useState, useEffect, useRef, ReactNode } from "react";
import "./Carousel.css";

interface CarouselProps {
  children: ReactNode[];
  navigation: "buttons" | "thumbnails" | "dot-thumbnails";
  infiniteScroll?: boolean;
  autoplay?: boolean;
  autoplaySpeed?: number;
  className?: string;
  style?: React.CSSProperties;
}

const Carousel: React.FC<CarouselProps> = ({
  children,
  navigation = "buttons",
  infiniteScroll = false,
  autoplay = false,
  autoplaySpeed = 3000,
  className = "",
  style = {},
}) => {
  const totalSlides = children.length;
  const extendedSlides = infiniteScroll
    ? [children[totalSlides - 1], ...children, children[0]] // Add extra first & last slide
    : children;

  const [currentIndex, setCurrentIndex] = useState(infiniteScroll ? 1 : 0); // Start at 1 for smooth looping
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const trackRef = useRef<HTMLDivElement>(null);
  const touchStartX = useRef<number | null>(null);

  useEffect(() => {
    if (!autoplay || isPaused) return;
    const interval = setInterval(() => nextSlide(), autoplaySpeed);
    return () => clearInterval(interval);
  }, [autoplay, autoplaySpeed, isPaused]);

  const nextSlide = () => {
    if (!isTransitioning) {
      setIsTransitioning(true);
      setCurrentIndex((prev) => prev + 1);
    }
  };

  const prevSlide = () => {
    if (!isTransitioning) {
      setIsTransitioning(true);
      setCurrentIndex((prev) => prev - 1);
    }
  };

  // Handle Infinite Scroll Reset
  useEffect(() => {
    if (!infiniteScroll) return;
    const transitionEnd = () => {
      setIsTransitioning(false);
      if (currentIndex === 0) {
        setCurrentIndex(totalSlides);
      } else if (currentIndex === totalSlides + 1) {
        setCurrentIndex(1);
      }
    };

    const track = trackRef.current;
    if (track) track.addEventListener("transitionend", transitionEnd);
    return () => {
      if (track) track.removeEventListener("transitionend", transitionEnd);
    };
  }, [currentIndex, infiniteScroll, totalSlides]);

  const handleTouchStart = (e: React.TouchEvent) => {
    touchStartX.current = e.touches[0].clientX;
  };

  const handleTouchEnd = (e: React.TouchEvent) => {
    if (!touchStartX.current) return;
    const touchEndX = e.changedTouches[0].clientX;
    const deltaX = touchStartX.current - touchEndX;

    if (Math.abs(deltaX) > 50) {
      deltaX > 0 ? nextSlide() : prevSlide();
    }
    touchStartX.current = null;
  };

  return (
    <div
      className={`carousel ${className}`}
      style={style}
      onMouseEnter={() => setIsPaused(true)}
      onMouseLeave={() => setIsPaused(false)}
      onTouchStart={handleTouchStart}
      onTouchEnd={handleTouchEnd}
    >
      <div
        className="carousel-track"
        ref={trackRef}
        style={{
          transform: `translateX(-${currentIndex * 100}%)`,
          transition: isTransitioning ? "transform 0.4s ease" : "none",
        }}
      >
        {extendedSlides.map((child, index) => (
          <div key={index} className="carousel-slide">
            {child}
          </div>
        ))}
      </div>

      <div className="carousel-navigations">
        {/* Handle thumbnail navigations */}
        {navigation === "thumbnails" && (
          <div className="thumbnails">
            {children.map((child, index) => {
              let ReactChild = child as React.ReactElement
              if (ReactChild.type === "img") {
                return (
                  <img
                    key={index}
                    src={(child as React.ReactElement).props.src}
                    alt={`Thumbnail ${index}`}
                    className={currentIndex === index ? "active" : ""}
                    onClick={() => setCurrentIndex(index)}
                  />
                )
              }
            })}
          </div>
        )}
        {/* Handle dot thumbnail navigations */}
        {navigation === "dot-thumbnails" && (
          <div className="dot-thumbnails">
            {children.map((child, index) => {
              return (
                <div
                  key={index}
                  className={currentIndex === index ? "dot active" : "dot"}
                  onClick={() => setCurrentIndex(index)}
                ></div>
              )
            })}
          </div>
        )}

        {/* Handle button navigations */}
        {navigation === "buttons" && (
          <div className="buttons">
            <button
              className="button prev"
              onClick={prevSlide}
              disabled={!infiniteScroll && currentIndex === 0}
            >
              <span className="arrow prev"></span>
            </button>
            <h6 className="carousel-items-status">
              {infiniteScroll
                ? (currentIndex === 0 ? totalSlides : currentIndex > totalSlides ? 1 : currentIndex)
                : currentIndex + 1
              }/{totalSlides}
            </h6>
            <button
              className="button next"
              onClick={nextSlide}
              disabled={!infiniteScroll && currentIndex === totalSlides - 1}
            >
              <span className="arrow next"></span>
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Carousel;
