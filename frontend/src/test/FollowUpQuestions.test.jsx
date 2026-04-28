import { render, screen, fireEvent } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import FollowUpQuestions from '../components/chat/FollowUpQuestions'

// Mock framer-motion
vi.mock('framer-motion', () => ({
  motion: {
    div: ({ children, ...props }) => <div {...props}>{children}</div>,
    button: ({ children, ...props }) => <button {...props}>{children}</button>,
  },
  AnimatePresence: ({ children }) => <>{children}</>,
}))

// Mock lucide-react icons
vi.mock('lucide-react', () => ({
  MessageCircle: () => <div data-testid="message-circle-icon" />,
  Sparkles: () => <div data-testid="sparkles-icon" />,
  ChevronRight: () => <div data-testid="chevron-right-icon" />,
}))

describe('FollowUpQuestions', () => {
  const mockQuestions = [
    'What is your full name?',
    'What is your email address?',
    'What are your top skills?',
  ]

  const mockOnQuestionClick = vi.fn()

  beforeEach(() => {
    mockOnQuestionClick.mockClear()
  })

  it('renders nothing when no questions provided', () => {
    const { container } = render(
      <FollowUpQuestions 
        questions={[]} 
        onQuestionClick={mockOnQuestionClick} 
        isLoading={false} 
      />
    )
    expect(container.firstChild).toBeNull()
  })

  it('renders loading skeleton when isLoading is true', () => {
    render(
      <FollowUpQuestions 
        questions={[]} 
        onQuestionClick={mockOnQuestionClick} 
        isLoading={true} 
      />
    )
    
    expect(screen.getByText('Generating personalized questions...')).toBeInTheDocument()
    expect(screen.getByTestId('sparkles-icon')).toBeInTheDocument()
  })

  it('renders questions when provided', () => {
    render(
      <FollowUpQuestions 
        questions={mockQuestions} 
        onQuestionClick={mockOnQuestionClick} 
        isLoading={false} 
      />
    )
    
    expect(screen.getByText('Suggested questions to help me understand better')).toBeInTheDocument()
    
    mockQuestions.forEach(question => {
      expect(screen.getByText(question)).toBeInTheDocument()
    })
  })

  it('calls onQuestionClick when a question is clicked', () => {
    render(
      <FollowUpQuestions 
        questions={mockQuestions} 
        onQuestionClick={mockOnQuestionClick} 
        isLoading={false} 
      />
    )
    
    const firstQuestionButton = screen.getByText(mockQuestions[0]).closest('button')
    fireEvent.click(firstQuestionButton)
    
    expect(mockOnQuestionClick).toHaveBeenCalledWith(mockQuestions[0])
    expect(mockOnQuestionClick).toHaveBeenCalledTimes(1)
  })

  it('disables buttons when isLoading is true', () => {
    render(
      <FollowUpQuestions 
        questions={mockQuestions} 
        onQuestionClick={mockOnQuestionClick} 
        isLoading={true} 
      />
    )
    
    // Should show loading skeleton, not question buttons
    expect(screen.queryByText(mockQuestions[0])).not.toBeInTheDocument()
  })

  it('renders helper text', () => {
    render(
      <FollowUpQuestions 
        questions={mockQuestions} 
        onQuestionClick={mockOnQuestionClick} 
        isLoading={false} 
      />
    )
    
    expect(screen.getByText('Click a question to answer it, or type your own message below')).toBeInTheDocument()
  })

  it('renders correct number of questions', () => {
    render(
      <FollowUpQuestions 
        questions={mockQuestions} 
        onQuestionClick={mockOnQuestionClick} 
        isLoading={false} 
      />
    )
    
    const questionButtons = screen.getAllByRole('button')
    expect(questionButtons).toHaveLength(mockQuestions.length)
  })

  it('renders icons for each question', () => {
    render(
      <FollowUpQuestions 
        questions={mockQuestions} 
        onQuestionClick={mockOnQuestionClick} 
        isLoading={false} 
      />
    )
    
    const messageIcons = screen.getAllByTestId('message-circle-icon')
    const chevronIcons = screen.getAllByTestId('chevron-right-icon')
    
    expect(messageIcons).toHaveLength(mockQuestions.length)
    expect(chevronIcons).toHaveLength(mockQuestions.length)
  })
})