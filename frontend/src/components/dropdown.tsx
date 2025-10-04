import { useState, useRef, useEffect } from "react";
import "../styles/dropdown.css";

type Props = {
  options: string[];
  value: number | null;
  onChange: (next: number) => void;
  onAction?: () => void; // opcional
  actionLabel?: string; // opcional (por defecto "Ir a otra página")
  onAdd?: () => void; // opcional
};

export default function Dropdown({
  options,
  value,
  onChange,
  onAction,
  actionLabel = "Ir a otra página",
  onAdd,
}: Props) {
  const [open, setOpen] = useState(false);
  const [focusIdx, setFocusIdx] = useState<number>(-1);
  const ref = useRef<HTMLDivElement>(null);
  const listId = "dropdown-listbox";

  // Cerrar al hacer click fuera
  useEffect(() => {
    const onClickOutside = (e: MouseEvent) => {
      if (ref.current && !ref.current.contains(e.target as Node)) {
        setOpen(false);
        setFocusIdx(-1);
      }
    };
    document.addEventListener("mousedown", onClickOutside);
    return () => document.removeEventListener("mousedown", onClickOutside);
  }, []);

  // Manejo de teclado
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (!open) {
      if (e.key === "ArrowDown" || e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        setOpen(true);
        setFocusIdx(0);
      }
      return;
    }

    if (e.key === "Escape") {
      e.preventDefault();
      setOpen(false);
      setFocusIdx(-1);
      return;
    }
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setFocusIdx((i) => Math.min(i + 1, options.length - 1));
      return;
    }
    if (e.key === "ArrowUp") {
      e.preventDefault();
      setFocusIdx((i) => Math.max(i - 1, 0));
      return;
    }
    if (e.key === "Enter") {
      e.preventDefault();
      if (focusIdx >= 0 && focusIdx < options.length) {
        onChange(focusIdx);
        setOpen(false);
        setFocusIdx(-1);
      }
      return;
    }
  };

  return (
    <div
      ref={ref}
      className="dropdown"
      onKeyDown={handleKeyDown}
    >
      <button
        type="button"
        aria-haspopup="listbox"
        aria-expanded={open}
        aria-controls={listId}
        onClick={() => {
          setOpen((o) => !o);
          if (!open) setFocusIdx(0);
        }}
        className="dropdown__btn"
      >
        {options[value ?? 0]}
        <span className="dropdown__caret">▼</span>
      </button>

      {open && (
        <ul
          id={listId}
          role="listbox"
          className="dropdown__list"
        >
          {options.map((op, idx) => {
            const focused = idx === focusIdx;

            return (
              <li
                key={op}
                role="option"
                tabIndex={-1}
                onMouseEnter={() => setFocusIdx(idx)}
                onClick={() => {
                  onChange(idx);
                  setOpen(false);
                  setFocusIdx(-1);
                }}
                className={`dropdown__option ${focused ? "dropdown__option--focus" : ""}`}
              >
                {op}
              </li>
            );
          })}

          {onAction && (
            <>
              <li className="dropdown__separator" />
              <li className="dropdown__action">
                <button
                  type="button"
                  onClick={() => {
                    onAction();
                    setOpen(false);
                    setFocusIdx(-1);
                  }}
                  className="btn"
                  style={{ width: "100%" }}
                >
                  {actionLabel}
                </button>
              </li>
            </>
          )}
          {onAdd && (
            <li className="dropdown__action">
              <button
                type="button"
                onClick={() => {
                  onAdd();
                  setOpen(false);
                  setFocusIdx(-1);
                }}
                className="btn"
                style={{ width: "100%" }}
              >
                ➕ Add
              </button>
            </li>
          )}
        </ul>
      )}
    </div>
  );
}