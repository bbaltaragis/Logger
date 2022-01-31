import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/services/api.service';
import { JsonpClientBackend } from '@angular/common/http';
import { Dashboard } from 'src/app/models/logview.models';
import { Router } from '@angular/router';
@Component({
  selector: 'app-logview',
  templateUrl: './logview.component.html',
  styleUrls: ['./logview.component.less']
})
export class LogviewComponent implements OnInit {
  dashboard: Dashboard;
  constructor(private _api : ApiService, private router: Router) { }
  
  ngOnInit(): void {
    this.getLogs();
  }

  getLogs(){
    this._api.getDashboard('dashboard').subscribe(
      (data) => {
        this.dashboard = data;
        console.log(this.dashboard);
      }
    );
  }

  viewAnomaly(id: number){
    console.log(id);
    let route = '/anomaly/'+id;
    this.router.navigate([route]);
  }

}
