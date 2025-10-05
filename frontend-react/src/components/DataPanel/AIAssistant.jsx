import { Bot, Send, Brain, Network, Lightbulb, Languages } from 'lucide-react'
import { useState, useRef, useEffect } from 'react'
import { useStore } from '../../store/useStore'

const suggestionQuestions = [
  'What is the climate like in this location?',
  'How can we reduce urban heat islands here?',
  'What are the environmental challenges in this area?',
]

export default function AIAssistant() {
  const [inputMessage, setInputMessage] = useState('')
  const messagesEndRef = useRef(null)
  const { chatMessages, sendChatMessage, selectedAreaData, analyzeSelectedArea, mapCenter, selectedArea } = useStore()

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [chatMessages])

  const handleSend = () => {
    if (!inputMessage.trim()) return

    sendChatMessage(inputMessage)
    setInputMessage('')
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const handleSuggestion = (question) => {
    setInputMessage(question)
  }

  return (
    <div className="bg-white/5 border border-white/10 rounded-xl p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <Bot className="w-6 h-6 text-primary-400" />
          <h3 className="text-primary-400 font-semibold">AI Urban Planning Assistant</h3>
        </div>
        <div className="flex items-center gap-2 text-xs text-gray-400">
          <div className="w-2 h-2 rounded-full bg-success-500 animate-pulse-slow"></div>
          <span>Ready</span>
          {(selectedArea || mapCenter) && (
            <div className="flex items-center gap-1 ml-2 text-primary-400">
              <div className="w-1.5 h-1.5 rounded-full bg-primary-400"></div>
              <span>Location-aware</span>
            </div>
          )}
        </div>
      </div>

      {/* Chat Messages */}
      <div className="bg-black/20 rounded-xl p-4 mb-4 h-[300px] overflow-y-auto scrollbar-thin">
        <div className="space-y-4">
          {chatMessages.map((message, index) => (
            <div
              key={index}
              className={`flex gap-3 ${message.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}
            >
              {message.role === 'assistant' && (
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary-600 to-primary-700 flex items-center justify-center flex-shrink-0">
                  <Bot className="w-4 h-4 text-white" />
                </div>
              )}
              <div
                className={`max-w-[80%] rounded-xl p-3 text-sm ${
                  message.role === 'user'
                    ? 'bg-gradient-to-br from-success-600 to-success-500 text-white'
                    : 'bg-white/10 text-white'
                }`}
              >
                <p className="whitespace-pre-wrap">{message.content}</p>
                <small className="block mt-2 text-xs opacity-70">
                  {message.role === 'user' ? 'You' : 'AI Assistant'}
                </small>
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="space-y-3">
        <div className="flex gap-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask about urban planning, environmental data, or city development..."
            className="flex-1 px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white text-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-400"
          />
          <button
            onClick={handleSend}
            disabled={!inputMessage.trim()}
            className="px-4 py-3 bg-gradient-to-r from-success-600 to-success-500 rounded-lg text-white transition-all hover:shadow-lg hover:shadow-success-500/30 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>

        {/* Suggestions */}
        <div className="flex flex-wrap gap-2">
          {suggestionQuestions.map((question, index) => (
            <button
              key={index}
              onClick={() => handleSuggestion(question)}
              className="px-3 py-1.5 bg-white/10 border border-white/20 rounded-full text-xs text-white transition-all hover:bg-white/20 hover:-translate-y-0.5"
            >
              {question.split(' ').slice(0, 3).join(' ')}...
            </button>
          ))}
          {selectedAreaData && (
            <button
              onClick={analyzeSelectedArea}
              className="px-3 py-1.5 bg-gradient-to-r from-primary-600 to-primary-500 rounded-full text-xs text-white font-medium transition-all hover:shadow-lg hover:shadow-primary-500/30"
            >
              Analyze Selected Area
            </button>
          )}
        </div>
      </div>

      {/* AI Features */}
      <div className="mt-6 pt-6 border-t border-white/10">
        <h4 className="text-primary-400 font-semibold text-sm mb-3">AI Capabilities</h4>
        <div className="grid grid-cols-2 gap-2">
          {[
            { icon: Brain, label: 'Deep Learning Analysis' },
            { icon: Network, label: 'Predictive Modeling' },
            { icon: Lightbulb, label: 'Smart Recommendations' },
            { icon: Languages, label: 'Natural Language Processing' },
          ].map((feature, index) => (
            <div
              key={index}
              className="flex items-center gap-2 p-2 bg-white/5 rounded-lg text-xs text-gray-400"
            >
              <feature.icon className="w-4 h-4 text-primary-400" />
              <span>{feature.label}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

