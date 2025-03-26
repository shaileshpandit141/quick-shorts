import React, { useState, useEffect, useRef, ReactNode } from "react";
import "./Carousel.css";

interface CarouselProps {
  children: ReactNode[];
  navigation: "thumbnails" | "buttons" | "dot-thumbnails";
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
  style = {}
}) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPaused, setIsPaused] = useState(false);
  const trackRef = useRef<HTMLDivElement>(null);
  const touchStartX = useRef<number | null>(null);
  const totalSlides = children.length;

  const nextSlide = () => {
    setCurrentIndex((prev) => {
      if (infiniteScroll) return (prev + 1) % totalSlides;
      return prev < totalSlides - 1 ? prev + 1 : prev;
    });
  };

  const prevSlide = () => {
    setCurrentIndex((prev) => {
      if (infiniteScroll) return (prev - 1 + totalSlides) % totalSlides;
      return prev > 0 ? prev - 1 : prev;
    });
  };

  useEffect(() => {
    if (!autoplay || isPaused) return;
    const interval = setInterval(() => nextSlide(), autoplaySpeed);
    return () => clearInterval(interval);
  }, [autoplay, autoplaySpeed, isPaused]);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "ArrowRight") nextSlide();
      if (e.key === "ArrowLeft") prevSlide();
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

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
        style={{ transform: `translateX(-${currentIndex * 100}%)` }}
      >
        {children.map((child, index) => (
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
            <h6 className="carousel-items-status">{currentIndex + 1}/{children.length}</h6>
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
