/**
 * ScratchCard.tsx
 * ===============
 * Design: Retro Carnival / Lottery Ticket
 * A canvas-based scratch-off card that works on both desktop (mouse) and mobile (touch).
 * Reveals an 18% discount code for LogoClothz.com underneath a silver scratch coating.
 * Triggers confetti + CTA when ~60% of the surface is scratched.
 */

import { useCallback, useEffect, useRef, useState } from "react";

interface ScratchCardProps {
  onRevealed: () => void;
}

export default function ScratchCard({ onRevealed }: ScratchCardProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const isDrawing = useRef(false);
  const [revealed, setRevealed] = useState(false);
  const [scratchPercent, setScratchPercent] = useState(0);
  const revealedRef = useRef(false);

  // Card dimensions — responsive
  const CARD_W = 340;
  const CARD_H = 180;
  const BRUSH_RADIUS = 28;
  const REVEAL_THRESHOLD = 0.60;

  const initCanvas = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Fill with opaque silver scratch coating — must fully hide the code below
    ctx.globalAlpha = 1;
    const gradient = ctx.createLinearGradient(0, 0, CARD_W, CARD_H);
    gradient.addColorStop(0, "#757575");
    gradient.addColorStop(0.25, "#BDBDBD");
    gradient.addColorStop(0.5, "#E8E8E8");
    gradient.addColorStop(0.75, "#BDBDBD");
    gradient.addColorStop(1, "#757575");
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, CARD_W, CARD_H);
    // Second pass to ensure full opacity
    ctx.fillStyle = "rgba(160,160,160,0.4)";
    ctx.fillRect(0, 0, CARD_W, CARD_H);

    // Subtle crosshatch texture
    ctx.strokeStyle = "rgba(150,150,150,0.3)";
    ctx.lineWidth = 0.5;
    for (let i = 0; i < CARD_W; i += 8) {
      ctx.beginPath();
      ctx.moveTo(i, 0);
      ctx.lineTo(i, CARD_H);
      ctx.stroke();
    }
    for (let j = 0; j < CARD_H; j += 8) {
      ctx.beginPath();
      ctx.moveTo(0, j);
      ctx.lineTo(CARD_W, j);
      ctx.stroke();
    }

    // Coin icon hint
    ctx.fillStyle = "rgba(60,60,60,0.7)";
    ctx.font = "bold 14px 'Source Sans 3', sans-serif";
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText("✦  SCRATCH HERE  ✦", CARD_W / 2, CARD_H / 2 - 10);
    ctx.font = "11px 'Source Sans 3', sans-serif";
    ctx.fillStyle = "rgba(60,60,60,0.5)";
    ctx.fillText("Use finger or mouse to scratch", CARD_W / 2, CARD_H / 2 + 14);
  }, []);

  useEffect(() => {
    initCanvas();
  }, [initCanvas]);

  const getPos = (
    e: MouseEvent | TouchEvent,
    canvas: HTMLCanvasElement
  ): { x: number; y: number } => {
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    if ("touches" in e) {
      const touch = e.touches[0];
      return {
        x: (touch.clientX - rect.left) * scaleX,
        y: (touch.clientY - rect.top) * scaleY,
      };
    }
    return {
      x: ((e as MouseEvent).clientX - rect.left) * scaleX,
      y: ((e as MouseEvent).clientY - rect.top) * scaleY,
    };
  };

  const scratch = useCallback(
    (e: MouseEvent | TouchEvent) => {
      if (!isDrawing.current || revealedRef.current) return;
      const canvas = canvasRef.current;
      if (!canvas) return;
      const ctx = canvas.getContext("2d");
      if (!ctx) return;

      const { x, y } = getPos(e, canvas);

      ctx.globalCompositeOperation = "destination-out";
      ctx.beginPath();
      ctx.arc(x, y, BRUSH_RADIUS, 0, Math.PI * 2);
      ctx.fill();
      ctx.globalCompositeOperation = "source-over";

      // Sample pixels to calculate scratch percentage
      const imageData = ctx.getImageData(0, 0, CARD_W, CARD_H);
      let transparent = 0;
      for (let i = 3; i < imageData.data.length; i += 4) {
        if (imageData.data[i] === 0) transparent++;
      }
      const total = CARD_W * CARD_H;
      const pct = transparent / total;
      setScratchPercent(Math.round(pct * 100));

      if (pct >= REVEAL_THRESHOLD && !revealedRef.current) {
        revealedRef.current = true;
        setRevealed(true);
        // Clear entire canvas for full reveal
        ctx.clearRect(0, 0, CARD_W, CARD_H);
        onRevealed();
      }
    },
    [onRevealed]
  );

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const onMouseDown = (e: MouseEvent) => {
      isDrawing.current = true;
      scratch(e);
    };
    const onMouseMove = (e: MouseEvent) => scratch(e);
    const onMouseUp = () => { isDrawing.current = false; };

    const onTouchStart = (e: TouchEvent) => {
      e.preventDefault();
      isDrawing.current = true;
      scratch(e);
    };
    const onTouchMove = (e: TouchEvent) => {
      e.preventDefault();
      scratch(e);
    };
    const onTouchEnd = () => { isDrawing.current = false; };

    canvas.addEventListener("mousedown", onMouseDown);
    canvas.addEventListener("mousemove", onMouseMove);
    window.addEventListener("mouseup", onMouseUp);
    canvas.addEventListener("touchstart", onTouchStart, { passive: false });
    canvas.addEventListener("touchmove", onTouchMove, { passive: false });
    canvas.addEventListener("touchend", onTouchEnd);

    return () => {
      canvas.removeEventListener("mousedown", onMouseDown);
      canvas.removeEventListener("mousemove", onMouseMove);
      window.removeEventListener("mouseup", onMouseUp);
      canvas.removeEventListener("touchstart", onTouchStart);
      canvas.removeEventListener("touchmove", onTouchMove);
      canvas.removeEventListener("touchend", onTouchEnd);
    };
  }, [scratch]);

  return (
    <div className="relative" style={{ width: CARD_W, height: CARD_H }}>
      {/* Revealed layer — the discount code underneath */}
      <div
        className="absolute inset-0 flex flex-col items-center justify-center rounded-lg"
        style={{
          background: "linear-gradient(135deg, #FFF8E7 0%, #FFF3D0 100%)",
          borderRadius: "8px",
        }}
      >
        {/* Sunburst SVG */}
        <div className="absolute inset-0 flex items-center justify-center overflow-hidden rounded-lg">
          <svg
            className="sunburst opacity-10"
            width="300"
            height="300"
            viewBox="0 0 300 300"
          >
            {Array.from({ length: 24 }).map((_, i) => (
              <line
                key={i}
                x1="150"
                y1="150"
                x2={150 + 150 * Math.cos((i * Math.PI * 2) / 24)}
                y2={150 + 150 * Math.sin((i * Math.PI * 2) / 24)}
                stroke="#C9A84C"
                strokeWidth="8"
              />
            ))}
          </svg>
        </div>

        <p
          className="text-xs font-semibold tracking-widest uppercase mb-1"
          style={{ color: "#8B1A1A", fontFamily: "'Source Sans 3', sans-serif" }}
        >
          Your Exclusive Code
        </p>
        <p
          className="text-4xl font-black tracking-widest"
          style={{
            fontFamily: "'Playfair Display', serif",
            color: "#8B1A1A",
            letterSpacing: "0.15em",
          }}
        >
          LOGO18
        </p>
        <p
          className="text-sm font-semibold mt-1"
          style={{ color: "#C9A84C", fontFamily: "'Source Sans 3', sans-serif" }}
        >
          18% OFF Your Order
        </p>
      </div>

      {/* Scratch coating canvas */}
      {!revealed && (
        <canvas
          ref={canvasRef}
          width={CARD_W}
          height={CARD_H}
          className="absolute inset-0 rounded-lg scratch-canvas scratch-hint"
          style={{ borderRadius: "8px", zIndex: 2 }}
        />
      )}

      {/* Progress hint */}
      {!revealed && scratchPercent > 5 && (
        <div
          className="absolute -bottom-7 left-0 right-0 flex justify-center"
          style={{ pointerEvents: "none" }}
        >
          <span
            className="text-xs font-semibold"
            style={{ color: "#C9A84C", fontFamily: "'Source Sans 3', sans-serif" }}
          >
            {scratchPercent}% scratched — keep going!
          </span>
        </div>
      )}
    </div>
  );
}
