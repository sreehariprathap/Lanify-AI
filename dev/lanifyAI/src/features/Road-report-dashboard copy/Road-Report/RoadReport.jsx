import { useEffect, useState } from 'react';
import { TrendingUp } from "lucide-react"
import { Area, AreaChart, CartesianGrid, XAxis } from "recharts"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"

const chartData = [
  { month: "January", safety_score: 78 },
  { month: "February", safety_score: 82 },
  { month: "March", safety_score: 80 },
  { month: "April", safety_score: 75 },
  { month: "May", safety_score: 77 },
  { month: "June", safety_score: 79 },
]

const chartConfig = {
  safety_score: {
    label: "Safety Score",
    color: "green",
  },
}

const RoadReport = () => {
  const vehicleId = 1;

  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    console.log('vehicleId:', vehicleId);
    if (vehicleId) {
      fetchDrivingReport(vehicleId);
    }
  }, [vehicleId]);

  const fetchDrivingReport = async (id) => {
    try {
      // Simulating API response
      const dummyData = {
        vehicle_id: id,
        total_alerts: 5,
        alerts_summary: "Harsh braking, Over speeding, Sudden acceleration",
        safety_score: 78,
        recommendations: "Drive at a consistent speed and avoid harsh braking.",
        traffic_violations: [
          { date: "2024-01-15", location: "Main St", category: "Over speeding", impact: "High" },
          { date: "2024-02-20", location: "2nd Ave", category: "Harsh braking", impact: "Medium" },
          { date: "2024-03-10", location: "3rd Blvd", category: "Sudden acceleration", impact: "Low" },
        ],
      };
      setTimeout(() => {
        setReportData(dummyData);
        setLoading(false);
      }, 1500);
    } catch (error) {
      console.error('Error fetching driving report:', error);
      setLoading(false);
    }
  };

  if (!vehicleId) {
    return <div className="text-red-500 text-center mt-4">No Vehicle ID provided in the URL.</div>;
  }

  return (
    <div className="mx-auto p-4 w-full">
      <div className="card bg-base-100 shadow-xl p-4 flex flex-row gap-5">
        {/* info card */}
        <div className="card-body">
          <h2 className="card-title text-xl font-semibold">Driving Behaviour Report</h2>
          <p className="text-gray-500">Vehicle ID: {vehicleId}</p>
          {loading ? (
            <div className="flex flex-col gap-2">
              <div className="skeleton h-6 w-3/4"></div>
              <div className="skeleton h-4 w-1/2"></div>
              <div className="skeleton h-4 w-full"></div>
            </div>
          ) : reportData ? (
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <span className="font-medium">Driving Alerts:</span>
                <span className="badge badge-error p-1 rounded-full">{reportData.total_alerts}</span>
              </div>
              <div>
                <span className="font-medium">Behaviour Summary:</span>
                <p className="text-gray-600">{reportData.alerts_summary}</p>
              </div>
              <div>
                <span className="font-medium">Performance Score:</span>
                <p className="text-lg font-bold text-green-600">{reportData.safety_score}</p>
              </div>
              <div>
                <span className="font-medium">Improvement Tips:</span>
                <p className="text-gray-600">{reportData.recommendations}</p>
              </div>
            </div>
          ) : (
            <p className="text-gray-500">Error loading driving behaviours report.</p>
          )}
        </div>
        {/* graph - driving behaviour trend  */}
        <Card className="border-none">
          <CardHeader>
            <CardTitle>Driving Behaviour Trend</CardTitle>
            <CardDescription>
              Displaying driving performance trends for the last 6 months
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ChartContainer config={chartConfig}>
              <AreaChart
                accessibilityLayer
                data={chartData}
                margin={{
                  left: 12,
                  right: 12,
                }}
              >
                <CartesianGrid vertical={false} />
                <XAxis
                  dataKey="month"
                  tickLine={false}
                  axisLine={false}
                  tickMargin={8}
                  tickFormatter={(value) => value.slice(0, 3)}
                />
                <ChartTooltip cursor={false} content={<ChartTooltipContent />} />
                <defs>
                  <linearGradient id="fillDesktop" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="green" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="green" stopOpacity={0.1} />
                  </linearGradient>
                  <linearGradient id="fillMobile" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="green" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="green" stopOpacity={0.1} />
                  </linearGradient>
                </defs>
                <Area
                  dataKey="safety_score"
                  type="natural"
                  fill="url(#fillMobile)"
                  fillOpacity={0.4}
                  stroke="green"
                  stackId="a"
                />
              </AreaChart>
            </ChartContainer>
          </CardContent>
          <CardFooter>
            <div className="flex w-full items-start gap-2 text-sm">
              <div className="grid gap-2">
                <div className="flex items-center gap-2 font-medium leading-none">
                  Driving performance improved by 5.2% this month{" "}
                  <TrendingUp className="h-4 w-4" />
                </div>
                <div className="flex items-center gap-2 leading-none text-muted-foreground">
                  Period: January - June 2024
                </div>
              </div>
            </div>
          </CardFooter>
        </Card>
        {/* traffic violations table */}
        <div className="overflow-x-auto">
          <table className="table">
            {/* head */}
            <thead>
              <tr>
                <th>#</th>
                <th>Date</th>
                <th>Location</th>
                <th>Violation Category</th>
                <th>Safety Impact</th>
              </tr>
            </thead>
            {reportData && reportData.traffic_violations ? (
              <tbody>
                {reportData.traffic_violations.map((violation, index) => (
                  <tr key={index} className={index % 2 === 0 ? "hover:bg-base-300" : ""}>
                    <th>{index + 1}</th>
                    <td>{violation.date}</td>
                    <td>{violation.location}</td>
                    <td>{violation.category}</td>
                    <td>{violation.impact}</td>
                  </tr>
                ))}
              </tbody>
            ) : (
              <tbody>
                <tr>
                  <td colSpan="5">No traffic violations recorded.</td>
                </tr>
              </tbody>
            )}
          </table>
        </div>
      </div>
    </div>
  );
};

export default RoadReport;
