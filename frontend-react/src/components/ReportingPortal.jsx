import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { reportingApi } from '../services/reportingApi'
import { 
  ArrowLeft, 
  MapPin, 
  FileText, 
  Upload, 
  Send,
  CheckCircle,
  AlertTriangle,
  Info,
  Camera,
  Calendar,
  User
} from 'lucide-react'

export default function ReportingPortal() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    reporterName: '',
    reporterEmail: '',
    reportType: 'environmental_issue',
    location: {
      address: '',
      latitude: '',
      longitude: ''
    },
    title: '',
    description: '',
    severity: 'medium',
    category: 'heat_island',
    date: new Date().toISOString().split('T')[0],
    images: [],
    contactPermission: false,
    followUp: false
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [isSubmitted, setIsSubmitted] = useState(false)

  const reportTypes = [
    { value: 'environmental_issue', label: 'Environmental Issue', icon: AlertTriangle },
    { value: 'flood_risk', label: 'Flood Risk', icon: AlertTriangle },
    { value: 'heat_stress', label: 'Heat Stress', icon: AlertTriangle },
    { value: 'air_quality', label: 'Air Quality Concern', icon: AlertTriangle },
    { value: 'green_space', label: 'Green Space Opportunity', icon: CheckCircle },
    { value: 'urban_planning', label: 'Urban Planning Suggestion', icon: Info },
    { value: 'infrastructure', label: 'Infrastructure Issue', icon: AlertTriangle }
  ]

  const categories = [
    { value: 'heat_island', label: 'Urban Heat Island' },
    { value: 'flooding', label: 'Flooding/Drainage' },
    { value: 'air_pollution', label: 'Air Pollution' },
    { value: 'green_coverage', label: 'Green Space' },
    { value: 'transportation', label: 'Transportation' },
    { value: 'waste_management', label: 'Waste Management' },
    { value: 'energy', label: 'Energy Efficiency' },
    { value: 'other', label: 'Other' }
  ]

  const handleInputChange = (field, value) => {
    if (field.includes('.')) {
      const [parent, child] = field.split('.')
      setFormData(prev => ({
        ...prev,
        [parent]: {
          ...prev[parent],
          [child]: value
        }
      }))
    } else {
      setFormData(prev => ({
        ...prev,
        [field]: value
      }))
    }
  }

  const handleImageUpload = (event) => {
    const files = Array.from(event.target.files)
    setFormData(prev => ({
      ...prev,
      images: [...prev.images, ...files]
    }))
  }

  const removeImage = (index) => {
    setFormData(prev => ({
      ...prev,
      images: prev.images.filter((_, i) => i !== index)
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsSubmitting(true)

    try {
      // Prepare report data for API
      const reportData = {
        reporter_name: formData.reporterName,
        reporter_email: formData.reporterEmail,
        report_type: formData.reportType,
        title: formData.title,
        description: formData.description,
        severity: formData.severity,
        category: formData.category,
        location: {
          address: formData.location.address,
          latitude: formData.location.latitude ? parseFloat(formData.location.latitude) : null,
          longitude: formData.location.longitude ? parseFloat(formData.location.longitude) : null
        },
        date_observed: new Date(formData.date).toISOString(),
        images: [], // Images would be uploaded separately in a real implementation
        contact_permission: formData.contactPermission,
        follow_up: formData.followUp
      }

      // Submit report to API
      const response = await reportingApi.submitReport(reportData)
      
      console.log('Report submitted successfully:', response)
      setIsSubmitted(true)
    } catch (error) {
      console.error('Error submitting report:', error)
      alert('Failed to submit report. Please try again.')
    } finally {
      setIsSubmitting(false)
    }
  }

  const resetForm = () => {
    setFormData({
      reporterName: '',
      reporterEmail: '',
      reportType: 'environmental_issue',
      location: {
        address: '',
        latitude: '',
        longitude: ''
      },
      title: '',
      description: '',
      severity: 'medium',
      category: 'heat_island',
      date: new Date().toISOString().split('T')[0],
      images: [],
      contactPermission: false,
      followUp: false
    })
    setIsSubmitted(false)
  }

  if (isSubmitted) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-900 via-primary-800 to-primary-700 flex items-center justify-center p-4">
        <div className="bg-white/10 backdrop-blur-lg border border-white/20 rounded-3xl p-12 max-w-2xl mx-auto text-center">
          <div className="bg-gradient-to-r from-green-500 to-green-600 p-6 rounded-full w-fit mx-auto mb-8">
            <CheckCircle className="w-16 h-16 text-white" />
          </div>
          <h1 className="text-4xl font-bold text-white mb-4">Report Submitted Successfully!</h1>
          <p className="text-primary-200 mb-8 text-lg">
            Thank you for contributing to urban resilience planning. Your report has been received and will be reviewed by our team.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={resetForm}
              className="bg-gradient-to-r from-blue-600 to-blue-700 text-white px-8 py-3 rounded-xl font-semibold hover:from-blue-700 hover:to-blue-800 transition-all duration-300"
            >
              Submit Another Report
            </button>
            <Link
              to="/"
              className="bg-white/10 text-white px-8 py-3 rounded-xl font-semibold border border-white/20 hover:bg-white/20 transition-all duration-300"
            >
              Back to Main Menu
            </Link>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-900 via-primary-800 to-primary-700 p-4">
      {/* Header */}
      <div className="max-w-6xl mx-auto mb-8">
        <div className="flex items-center gap-4 mb-6">
          <Link
            to="/"
            className="bg-white/10 backdrop-blur-lg border border-white/20 rounded-xl p-3 hover:bg-white/20 transition-all duration-300"
          >
            <ArrowLeft className="w-6 h-6 text-white" />
          </Link>
          <div>
            <h1 className="text-4xl font-bold text-white">Reporting Portal</h1>
            <p className="text-primary-200">Contribute to urban resilience planning</p>
          </div>
        </div>
      </div>

      {/* Form */}
      <div className="max-w-4xl mx-auto">
        <div className="bg-white/10 backdrop-blur-lg border border-white/20 rounded-3xl p-8">
          <form onSubmit={handleSubmit} className="space-y-8">
            {/* Reporter Information */}
            <div className="space-y-6">
              <h2 className="text-2xl font-bold text-white flex items-center gap-3">
                <User className="w-6 h-6" />
                Reporter Information
              </h2>
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-primary-200 font-semibold mb-2">Full Name *</label>
                  <input
                    type="text"
                    required
                    value={formData.reporterName}
                    onChange={(e) => handleInputChange('reporterName', e.target.value)}
                    className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white placeholder-primary-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Enter your full name"
                  />
                </div>
                <div>
                  <label className="block text-primary-200 font-semibold mb-2">Email Address *</label>
                  <input
                    type="email"
                    required
                    value={formData.reporterEmail}
                    onChange={(e) => handleInputChange('reporterEmail', e.target.value)}
                    className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white placeholder-primary-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Enter your email"
                  />
                </div>
              </div>
            </div>

            {/* Report Details */}
            <div className="space-y-6">
              <h2 className="text-2xl font-bold text-white flex items-center gap-3">
                <FileText className="w-6 h-6" />
                Report Details
              </h2>
              
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-primary-200 font-semibold mb-2">Report Type *</label>
                  <select
                    required
                    value={formData.reportType}
                    onChange={(e) => handleInputChange('reportType', e.target.value)}
                    className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    {reportTypes.map(type => (
                      <option key={type.value} value={type.value} className="bg-primary-800">
                        {type.label}
                      </option>
                    ))}
                  </select>
                </div>
                
                <div>
                  <label className="block text-primary-200 font-semibold mb-2">Severity Level *</label>
                  <select
                    required
                    value={formData.severity}
                    onChange={(e) => handleInputChange('severity', e.target.value)}
                    className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="low" className="bg-primary-800">Low</option>
                    <option value="medium" className="bg-primary-800">Medium</option>
                    <option value="high" className="bg-primary-800">High</option>
                    <option value="critical" className="bg-primary-800">Critical</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-primary-200 font-semibold mb-2">Report Title *</label>
                <input
                  type="text"
                  required
                  value={formData.title}
                  onChange={(e) => handleInputChange('title', e.target.value)}
                  className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white placeholder-primary-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Brief title describing the issue"
                />
              </div>

              <div>
                <label className="block text-primary-200 font-semibold mb-2">Description *</label>
                <textarea
                  required
                  rows={4}
                  value={formData.description}
                  onChange={(e) => handleInputChange('description', e.target.value)}
                  className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white placeholder-primary-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Detailed description of the issue, including impact and context..."
                />
              </div>

              <div>
                <label className="block text-primary-200 font-semibold mb-2">Category *</label>
                <select
                  required
                  value={formData.category}
                  onChange={(e) => handleInputChange('category', e.target.value)}
                  className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  {categories.map(category => (
                    <option key={category.value} value={category.value} className="bg-primary-800">
                      {category.label}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Location */}
            <div className="space-y-6">
              <h2 className="text-2xl font-bold text-white flex items-center gap-3">
                <MapPin className="w-6 h-6" />
                Location Information
              </h2>
              
              <div>
                <label className="block text-primary-200 font-semibold mb-2">Address/Location *</label>
                <input
                  type="text"
                  required
                  value={formData.location.address}
                  onChange={(e) => handleInputChange('location.address', e.target.value)}
                  className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white placeholder-primary-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Street address, landmark, or area description"
                />
              </div>

              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-primary-200 font-semibold mb-2">Latitude (Optional)</label>
                  <input
                    type="number"
                    step="any"
                    value={formData.location.latitude}
                    onChange={(e) => handleInputChange('location.latitude', e.target.value)}
                    className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white placeholder-primary-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="e.g., 2.3000"
                  />
                </div>
                <div>
                  <label className="block text-primary-200 font-semibold mb-2">Longitude (Optional)</label>
                  <input
                    type="number"
                    step="any"
                    value={formData.location.longitude}
                    onChange={(e) => handleInputChange('location.longitude', e.target.value)}
                    className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white placeholder-primary-300 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="e.g., 111.8200"
                  />
                </div>
              </div>
            </div>

            {/* Images */}
            <div className="space-y-6">
              <h2 className="text-2xl font-bold text-white flex items-center gap-3">
                <Camera className="w-6 h-6" />
                Supporting Images (Optional)
              </h2>
              
              <div className="border-2 border-dashed border-white/20 rounded-xl p-8 text-center">
                <input
                  type="file"
                  multiple
                  accept="image/*"
                  onChange={handleImageUpload}
                  className="hidden"
                  id="image-upload"
                />
                <label htmlFor="image-upload" className="cursor-pointer">
                  <Upload className="w-12 h-12 text-primary-300 mx-auto mb-4" />
                  <p className="text-primary-200 mb-2">Click to upload images or drag and drop</p>
                  <p className="text-primary-300 text-sm">PNG, JPG, JPEG up to 10MB each</p>
                </label>
              </div>

              {formData.images.length > 0 && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  {formData.images.map((image, index) => (
                    <div key={index} className="relative">
                      <img
                        src={URL.createObjectURL(image)}
                        alt={`Upload ${index + 1}`}
                        className="w-full h-24 object-cover rounded-lg"
                      />
                      <button
                        type="button"
                        onClick={() => removeImage(index)}
                        className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs hover:bg-red-600"
                      >
                        ×
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Additional Options */}
            <div className="space-y-4">
              <h2 className="text-2xl font-bold text-white flex items-center gap-3">
                <Calendar className="w-6 h-6" />
                Additional Information
              </h2>
              
              <div>
                <label className="block text-primary-200 font-semibold mb-2">Date of Observation *</label>
                <input
                  type="date"
                  required
                  value={formData.date}
                  onChange={(e) => handleInputChange('date', e.target.value)}
                  className="w-full bg-white/10 border border-white/20 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div className="space-y-4">
                <label className="flex items-center gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={formData.contactPermission}
                    onChange={(e) => handleInputChange('contactPermission', e.target.checked)}
                    className="w-5 h-5 text-blue-600 bg-white/10 border-white/20 rounded focus:ring-blue-500"
                  />
                  <span className="text-primary-200">I give permission to be contacted for follow-up information</span>
                </label>

                <label className="flex items-center gap-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={formData.followUp}
                    onChange={(e) => handleInputChange('followUp', e.target.checked)}
                    className="w-5 h-5 text-blue-600 bg-white/10 border-white/20 rounded focus:ring-blue-500"
                  />
                  <span className="text-primary-200">I would like to receive updates about this report</span>
                </label>
              </div>
            </div>

            {/* Submit Button */}
            <div className="flex justify-end pt-6">
              <button
                type="submit"
                disabled={isSubmitting}
                className="bg-gradient-to-r from-green-600 to-green-700 text-white px-12 py-4 rounded-xl font-semibold hover:from-green-700 hover:to-green-800 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-3"
              >
                {isSubmitting ? (
                  <>
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    Submitting...
                  </>
                ) : (
                  <>
                    <Send className="w-5 h-5" />
                    Submit Report
                  </>
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}
