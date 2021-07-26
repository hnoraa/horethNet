import { Component, OnInit } from '@angular/core';
import { HttpService } from './services/http/http.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'frontend';
  constructor (private server: HttpService) {}

  ngOnInit() {
    this.server.test().subscribe((data: string) => {
      this.title = data;
      console.log(data);
    });
  }
}
