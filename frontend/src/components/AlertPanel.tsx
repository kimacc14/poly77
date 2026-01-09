interface Alert {
  id: number;
  alert_type: string;
  topic: string;
  message: string;
  severity: string;
  created_at: string;
  read: boolean;
}

export default function AlertPanel({ alerts }: { alerts: Alert[] }) {
  if (alerts.length === 0) {
    return null;
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high':
        return 'bg-red-50 border-red-200 text-red-800';
      case 'medium':
        return 'bg-yellow-50 border-yellow-200 text-yellow-800';
      default:
        return 'bg-blue-50 border-blue-200 text-blue-800';
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'high':
        return '🔴';
      case 'medium':
        return '🟡';
      default:
        return '🔵';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Alerts</h2>

      <div className="space-y-3">
        {alerts.slice(0, 5).map(alert => (
          <div
            key={alert.id}
            className={`p-4 rounded-lg border-l-4 ${getSeverityColor(alert.severity)}`}
          >
            <div className="flex items-start gap-3">
              <span className="text-2xl">{getSeverityIcon(alert.severity)}</span>
              <div className="flex-1">
                <div className="flex items-center justify-between mb-1">
                  <span className="font-semibold text-sm uppercase tracking-wide">
                    {alert.topic}
                  </span>
                  <span className="text-xs opacity-75">
                    {new Date(alert.created_at).toLocaleTimeString()}
                  </span>
                </div>
                <p className="text-sm">{alert.message}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {alerts.length > 5 && (
        <button className="mt-4 text-sm text-primary-600 hover:text-primary-700 font-medium">
          View all {alerts.length} alerts →
        </button>
      )}
    </div>
  );
}
