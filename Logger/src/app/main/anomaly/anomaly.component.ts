import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Anomaly } from 'src/app/models/anomaly.model';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-anomaly',
  templateUrl: './anomaly.component.html',
  styleUrls: ['./anomaly.component.less']
})
export class AnomalyComponent implements OnInit {
  public id: string;
  public anomaly: Anomaly;
  public comment: string;
  constructor(private router: Router, private _api : ApiService, private route:ActivatedRoute) { }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.id = params['id'];
    })

    this.getAnomaly()
  }

  getDashboard(){
    this.router.navigate(['/logview']);
  }

  getAnomaly(){
    console.log(this.id);
    this._api.getAnomaly(this.id).subscribe(
      (data) => {
        this.anomaly = new Anomaly();
        this.anomaly = data;
        console.log(this.anomaly);
      }
    );
  }

  postComment(comment: string){
    console.log(comment);
    console.log(this.id);
    this._api.postComment(comment, this.id).subscribe(
      (data) => {
        this.getAnomaly();
      }
    );
  }

  patchResolutionSteps(resolution: string){
    console.log(resolution);
    console.log(this.id);
    this._api.patchResolutionSteps(resolution, this.id).subscribe(
      (data) => {
        this.getAnomaly();
      }
    );
  }

  patchRootCause(rootCause: string){
    console.log(rootCause);
    console.log(this.id);
    this._api.patchRootCause(rootCause, this.id).subscribe(
      (data) => {
        this.getAnomaly();
      }
    );
  }

}
