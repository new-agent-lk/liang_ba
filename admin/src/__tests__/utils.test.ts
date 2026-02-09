import { describe, it, expect, vi, beforeEach } from 'vitest'
import { formatCurrency, formatDate, truncate, debounce } from '../utils'

describe('formatCurrency', () => {
  it('formats positive numbers with currency symbol', () => {
    expect(formatCurrency(1234.56)).toBe('¥1,234.56')
  })

  it('formats zero correctly', () => {
    expect(formatCurrency(0)).toBe('¥0.00')
  })

  it('formats negative numbers correctly', () => {
    expect(formatCurrency(-1234.56)).toBe('¥-1,234.56')
  })
})

describe('formatDate', () => {
  it('formats date strings correctly', () => {
    expect(formatDate('2024-01-15')).toBe('2024-01-15')
  })

  it('handles empty strings', () => {
    expect(formatDate('')).toBe('')
  })
})

describe('truncate', () => {
  it('truncates long strings with ellipsis', () => {
    const longString = 'This is a very long string that needs truncating'
    expect(truncate(longString, 20)).toBe('This is a very long...')
  })

  it('returns short strings unchanged', () => {
    const shortString = 'Hi'
    expect(truncate(shortString, 20)).toBe('Hi')
  })

  it('handles maxLength equal to string length', () => {
    const str = 'Hi'
    expect(truncate(str, 2)).toBe('Hi')
  })
})

describe('debounce', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })

  afterEach(() => {
    vi.useRealTimers()
  })

  it('delays function execution', () => {
    const fn = vi.fn()
    const debouncedFn = debounce(fn, 100)

    debouncedFn()
    debouncedFn()
    debouncedFn()

    expect(fn).not.toHaveBeenCalled()

    vi.advanceTimersByTime(100)

    expect(fn).toHaveBeenCalledTimes(1)
  })

  it('calls function with latest arguments', () => {
    const fn = vi.fn()
    const debouncedFn = debounce(fn, 100)

    debouncedFn(1)
    debouncedFn(2)
    debouncedFn(3)

    vi.advanceTimersByTime(100)

    expect(fn).toHaveBeenCalledWith(3)
  })
})
