type Campo = {
  key: string;
  label: string;
  min?: number;
  max?: number;
  decimals?: number;
};

export const PERFILES: Record<number, Campo[]> = {
  0: [
        { key: "koi_period", label: "Period (days)", min: 0.2, max: 1000, decimals: 3 },
        { key: "koi_time0bk", label: "Transit epoch (BKJD)", min: 0, max: 1500, decimals: 5 },
        { key: "koi_impact", label: "Impact parameter", min: 0, max: 1.1, decimals: 3 },
        { key: "koi_duration", label: "Duration (hrs)", min: 0.5, max: 30, decimals: 2 },
        { key: "koi_depth", label: "Depth (ppm)", min: 20, max: 30000, decimals: 0 },
        { key: "koi_prad", label: "Planet radius (R⊕)", min: 0.3, max: 20, decimals: 3 },
        { key: "koi_teq", label: "Equilibrium temperature (K)", min: 100, max: 3500, decimals: 0 },
        { key: "koi_insol", label: "Insolation flux (S⊕)", min: 0.01, max: 5000, decimals: 2 },
        { key: "koi_model_snr", label: "Signal-to-noise ratio", min: 5, max: 1000, decimals: 2 },
        { key: "koi_steff", label: "Stellar effective temperature (K)", min: 3000, max: 7500, decimals: 0 },
        { key: "koi_srad", label: "Stellar radius (R☉)", min: 0.2, max: 3, decimals: 3 },
  ]
};