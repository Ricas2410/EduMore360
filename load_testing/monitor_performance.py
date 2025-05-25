"""
Real-time performance monitoring during load testing
"""

import psutil
import time
import requests
import json
from datetime import datetime
import threading

class PerformanceMonitor:
    def __init__(self, target_url="http://127.0.0.1:8000"):
        self.target_url = target_url
        self.monitoring = False
        self.results = []
        
    def check_response_time(self):
        """Check response time of key endpoints"""
        endpoints = [
            "/",
            "/dashboard/",
            "/quiz/",
            "/curriculum/",
            "/my-admin/"
        ]
        
        response_times = {}
        
        for endpoint in endpoints:
            try:
                start_time = time.time()
                response = requests.get(f"{self.target_url}{endpoint}", timeout=30)
                end_time = time.time()
                
                response_times[endpoint] = {
                    'response_time': round((end_time - start_time) * 1000, 2),  # ms
                    'status_code': response.status_code,
                    'success': response.status_code == 200
                }
            except Exception as e:
                response_times[endpoint] = {
                    'response_time': None,
                    'status_code': None,
                    'success': False,
                    'error': str(e)
                }
        
        return response_times
    
    def get_system_stats(self):
        """Get current system statistics"""
        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_available = round(memory.available / (1024**3), 2)  # GB
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            # Network stats
            network = psutil.net_io_counters()
            
            return {
                'timestamp': datetime.now().isoformat(),
                'cpu_percent': cpu_percent,
                'memory_percent': memory_percent,
                'memory_available_gb': memory_available,
                'disk_percent': disk_percent,
                'network_bytes_sent': network.bytes_sent,
                'network_bytes_recv': network.bytes_recv
            }
        except Exception as e:
            return {'error': str(e)}
    
    def monitor_loop(self):
        """Main monitoring loop"""
        print("🔍 Starting performance monitoring...")
        print("=" * 60)
        
        while self.monitoring:
            # Get system stats
            system_stats = self.get_system_stats()
            
            # Get response times
            response_times = self.check_response_time()
            
            # Combine data
            monitoring_data = {
                'system': system_stats,
                'response_times': response_times
            }
            
            self.results.append(monitoring_data)
            
            # Display current stats
            self.display_stats(system_stats, response_times)
            
            # Wait before next check
            time.sleep(10)  # Check every 10 seconds
    
    def display_stats(self, system_stats, response_times):
        """Display current statistics"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        print(f"\n⏰ {timestamp}")
        print("-" * 40)
        
        # System stats
        if 'error' not in system_stats:
            print(f"🖥️  CPU: {system_stats['cpu_percent']:.1f}%")
            print(f"💾 Memory: {system_stats['memory_percent']:.1f}% ({system_stats['memory_available_gb']:.1f}GB free)")
            print(f"💿 Disk: {system_stats['disk_percent']:.1f}%")
        else:
            print(f"❌ System stats error: {system_stats['error']}")
        
        # Response times
        print("\n🌐 Response Times:")
        for endpoint, data in response_times.items():
            if data['success']:
                status = "✅" if data['response_time'] < 2000 else "⚠️" if data['response_time'] < 5000 else "❌"
                print(f"   {status} {endpoint}: {data['response_time']}ms")
            else:
                print(f"   ❌ {endpoint}: ERROR ({data.get('error', 'Unknown error')})")
    
    def start_monitoring(self):
        """Start monitoring in background thread"""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self.monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        print("🚀 Performance monitoring started!")
        print("Press Ctrl+C to stop monitoring")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_monitoring()
    
    def stop_monitoring(self):
        """Stop monitoring and save results"""
        print("\n🛑 Stopping performance monitoring...")
        self.monitoring = False
        
        # Save results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"load_testing/performance_results_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2)
            print(f"📊 Results saved to: {filename}")
        except Exception as e:
            print(f"❌ Error saving results: {e}")
        
        # Display summary
        self.display_summary()
    
    def display_summary(self):
        """Display monitoring summary"""
        if not self.results:
            print("No data collected")
            return
        
        print("\n" + "=" * 60)
        print("📊 PERFORMANCE SUMMARY")
        print("=" * 60)
        
        # Calculate averages
        cpu_values = [r['system']['cpu_percent'] for r in self.results if 'cpu_percent' in r['system']]
        memory_values = [r['system']['memory_percent'] for r in self.results if 'memory_percent' in r['system']]
        
        if cpu_values:
            avg_cpu = sum(cpu_values) / len(cpu_values)
            max_cpu = max(cpu_values)
            print(f"🖥️  CPU Usage - Avg: {avg_cpu:.1f}%, Max: {max_cpu:.1f}%")
        
        if memory_values:
            avg_memory = sum(memory_values) / len(memory_values)
            max_memory = max(memory_values)
            print(f"💾 Memory Usage - Avg: {avg_memory:.1f}%, Max: {max_memory:.1f}%")
        
        # Response time summary
        print("\n🌐 Response Time Summary:")
        endpoints = ["/", "/dashboard/", "/quiz/", "/curriculum/", "/my-admin/"]
        
        for endpoint in endpoints:
            times = []
            errors = 0
            
            for result in self.results:
                if endpoint in result['response_times']:
                    rt_data = result['response_times'][endpoint]
                    if rt_data['success'] and rt_data['response_time']:
                        times.append(rt_data['response_time'])
                    else:
                        errors += 1
            
            if times:
                avg_time = sum(times) / len(times)
                max_time = max(times)
                min_time = min(times)
                success_rate = (len(times) / (len(times) + errors)) * 100
                
                status = "✅" if avg_time < 2000 and success_rate > 95 else "⚠️" if avg_time < 5000 and success_rate > 90 else "❌"
                print(f"   {status} {endpoint}:")
                print(f"      Avg: {avg_time:.0f}ms, Min: {min_time:.0f}ms, Max: {max_time:.0f}ms")
                print(f"      Success Rate: {success_rate:.1f}%")
        
        # Recommendations
        print("\n💡 RECOMMENDATIONS:")
        
        if cpu_values and max(cpu_values) > 80:
            print("   ⚠️  High CPU usage detected - consider optimizing code or scaling")
        
        if memory_values and max(memory_values) > 80:
            print("   ⚠️  High memory usage detected - check for memory leaks")
        
        # Check response times
        all_response_times = []
        for result in self.results:
            for endpoint, data in result['response_times'].items():
                if data['success'] and data['response_time']:
                    all_response_times.append(data['response_time'])
        
        if all_response_times:
            avg_response = sum(all_response_times) / len(all_response_times)
            if avg_response > 5000:
                print("   ❌ Slow response times - optimize database queries and caching")
            elif avg_response > 2000:
                print("   ⚠️  Response times could be improved - consider optimization")
            else:
                print("   ✅ Good response times!")

def main():
    """Main function"""
    import sys
    
    # Get target URL from command line or use default
    target_url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
    
    print("🧪 EduMore360 Performance Monitor")
    print("=" * 60)
    print(f"Target URL: {target_url}")
    print("Monitoring system performance and response times...")
    print("This will help you verify if your system can handle 2000 users")
    print("=" * 60)
    
    monitor = PerformanceMonitor(target_url)
    monitor.start_monitoring()

if __name__ == "__main__":
    main()
