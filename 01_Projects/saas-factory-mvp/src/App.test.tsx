import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from './App';

describe('App component', () => {
  it('renders progress text correctly', () => {
    render(<App />);
    const heading = screen.getByText(/SaaS Factory MVP/i);
    expect(heading).toBeInTheDocument();
  });

  it('renders the hero section with industrial speed message', () => {
    render(<App />);
    const heroText = screen.getByText(/Industrial Speed/i);
    expect(heroText).toBeInTheDocument();
  });
});
