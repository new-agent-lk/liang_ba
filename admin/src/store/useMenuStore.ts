import { create } from "zustand";

interface MenuState {
  collapsed: boolean;
  mobileOpen: boolean;
  setCollapsed: (collapsed: boolean) => void;
  toggleCollapsed: () => void;
  setMobileOpen: (open: boolean) => void;
  openMobileMenu: () => void;
  closeMobileMenu: () => void;
}

export const useMenuStore = create<MenuState>((set) => ({
  collapsed: false,
  mobileOpen: false,
  setCollapsed: (collapsed) => set({ collapsed }),
  toggleCollapsed: () => set((state) => ({ collapsed: !state.collapsed })),
  setMobileOpen: (mobileOpen) => set({ mobileOpen }),
  openMobileMenu: () => set({ mobileOpen: true }),
  closeMobileMenu: () => set({ mobileOpen: false }),
}));
