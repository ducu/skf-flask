import {Component, ElementRef, OnDestroy, OnInit, ViewChild} from '@angular/core';
import {TrainingService} from '../../../core/services/training.service';
import {ActivatedRoute, Router} from '@angular/router';
import {Subscription} from 'rxjs';
import {Course, Profile} from '../../../core/models/course.model';
import {NgxSpinnerService} from 'ngx-spinner';
import {UserService} from '../../../core/services/user.service';
import {TrainingNavigationService} from '../../../core/services/training-navigation.service';


@Component({
  selector: 'app-training-course',
  templateUrl: './training-course.component.html',
  styleUrls: ['./training-course.component.scss']
})
export class TrainingCourseComponent implements OnInit, OnDestroy {
  @ViewChild('rightSide') private rightSide: ElementRef;
  public userId: string;
  public profile: Profile;
  public course: Course;
  private subscriptions: Subscription[] = [];

  constructor(private trainingService: TrainingService,
              private trainingNavigationService: TrainingNavigationService,
              private userService: UserService,
              private activatedRoute: ActivatedRoute,
              private router: Router,
              private spinner: NgxSpinnerService) {
  }

  ngOnInit(): void {
    this.spinner.show();
    this.subscriptions.push(this.activatedRoute.params.subscribe(params => {
      const profileId = params['pid'];
      const courseId = params['cid'];
      this.subscriptions.push(this.trainingService.getProfileInfo(profileId).subscribe(profile => {
        this.profile = profile;
        if (this.course) {
          this.spinner.hide();
        }
      }));
      this.subscriptions.push(this.trainingService.getCourse(courseId).subscribe(course => {
        this.course = course;
        if (this.profile) {
          this.spinner.hide();
        }
      }));
    }));
    this.subscriptions.push(this.trainingNavigationService.openFullScreen$.subscribe(() => {
      this.openFullscreen();
    }));
    this.subscriptions.push(this.trainingNavigationService.closeFullScreen$.subscribe(() => {
      this.closeFullscreen();
    }));
  }

  private openFullscreen() {
    const elem = this.rightSide.nativeElement;
    if (elem.requestFullscreen) {
      elem.requestFullscreen();
    } else if (elem.webkitRequestFullscreen) { /* Safari */
      elem.webkitRequestFullscreen();
    } else if (elem.msRequestFullscreen) { /* IE11 */
      elem.msRequestFullscreen();
    }
  }

  private closeFullscreen() {
    const doc = document as any;
    if (doc.exitFullscreen) {
      doc.exitFullscreen();
    } else if (doc.webkitExitFullscreen) { /* Safari */
      doc.webkitExitFullscreen();
    } else if (doc.msExitFullscreen) { /* IE11 */
      doc.msExitFullscreen();
    }
  }

  goToTraining() {
    this.router.navigate(['training', 'profiles']);
  }

  goToProfile() {
    this.router.navigate(['training', 'profile', this.profile.id]);
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach(sub => {
      if (sub) {
        sub.unsubscribe();
      }
    });
  }
}
